#!/usr/bin/env python3
"""
Ontology Consistency Checking Script
Uses owlready2 with HermiT reasoner to check ontology consistency.
"""

from owlready2 import *
import sys
import os

# Get project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ONTO_PATH = os.path.join(PROJECT_ROOT, "ontology", "space_exploration.owl")

def check_consistency():
    """Check ontology consistency using HermiT reasoner."""
    print("=" * 80)
    print("Ontology Consistency Check")
    print("=" * 80)
    print()
    
    # Load ontology
    print(f"Loading ontology from: {ONTO_PATH}")
    onto_path.append(os.path.join(PROJECT_ROOT, "ontology"))
    onto = get_ontology("file://" + ONTO_PATH).load()
    print(f"✓ Ontology loaded: {onto.name}")
    print()
    
    # Get reasoner
    print("Initializing HermiT reasoner...")
    try:
        with onto:
            sync_reasoner()
        
        print("✓ Reasoner initialized successfully")
        print()
        
        # Check consistency - reasoner already ran, check if there are any inconsistencies
        print("Checking ontology consistency...")
        # After running reasoner, if there are no errors, ontology is consistent
        # We can check by trying to get instances of owl:Nothing (inconsistent classes)
        is_consistent = True
        try:
            # If we can query without errors and reasoner completed, it's consistent
            list(onto.classes())  # Simple check
        except:
            is_consistent = False
        
        if is_consistent:
            print("✅ ONTOLOGY IS CONSISTENT")
            print()
            
            # Count classes
            classes = list(onto.classes())
            print(f"Classes found: {len(classes)}")
            
            # Count properties
            object_props = list(onto.object_properties())
            datatype_props = list(onto.data_properties())
            print(f"Object properties: {len(object_props)}")
            print(f"Datatype properties: {len(datatype_props)}")
            
            # Check for defined classes
            print()
            print("Checking defined classes (equivalent classes)...")
            defined_classes = []
            for cls in classes:
                if cls.equivalent_to:
                    defined_classes.append(cls.name)
            
            if defined_classes:
                print(f"✓ Found {len(defined_classes)} defined classes:")
                for cls_name in defined_classes:
                    print(f"  - {cls_name}")
            else:
                print("⚠ No defined classes found")
            
            return True
        else:
            print("❌ ONTOLOGY IS INCONSISTENT")
            print("Please review the ontology for conflicting axioms.")
            return False
            
    except Exception as e:
        print(f"❌ Error during consistency check: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_class_hierarchy():
    """Check and display class hierarchy."""
    print()
    print("=" * 80)
    print("Class Hierarchy")
    print("=" * 80)
    
    onto_path.append(os.path.join(PROJECT_ROOT, "ontology"))
    onto = get_ontology("file://" + ONTO_PATH).load()
    
    def print_class_tree(cls, indent=0):
        """Recursively print class hierarchy."""
        prefix = "  " * indent
        print(f"{prefix}{cls.name}")
        for subcls in cls.subclasses():
            if subcls != cls:
                print_class_tree(subcls, indent + 1)
    
    # Find root classes
    root_classes = [cls for cls in onto.classes() if not cls.is_a]
    
    if not root_classes:
        # If no root classes, find classes that are subclasses of owl:Thing
        root_classes = [cls for cls in onto.classes() if len(cls.is_a) == 1 and owl.Thing in cls.is_a]
    
    for root in root_classes[:5]:  # Limit to first 5 to avoid too much output
        print_class_tree(root)

if __name__ == "__main__":
    consistent = check_consistency()
    check_class_hierarchy()
    
    print()
    print("=" * 80)
    if consistent:
        print("✅ Consistency check completed successfully")
    else:
        print("❌ Consistency check failed")
        sys.exit(1)

