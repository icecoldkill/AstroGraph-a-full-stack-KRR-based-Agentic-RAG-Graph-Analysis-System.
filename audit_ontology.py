import argparse
from owlready2 import *
import sys

def audit_ontology(ontology_path):
    print(f"🔍 Starting Audit for: {ontology_path}")
    
    try:
        onto = get_ontology(ontology_path).load()
    except Exception as e:
        print(f"❌ Failed to load ontology: {e}")
        return

    # 1. Classes Check (Target: 20+)
    classes = list(onto.classes())
    print(f"\n📊 Classes Count: {len(classes)} / 20")
    for c in classes:
        print(f"  - {c.name}")
    
    if len(classes) >= 20: print("  ✅ PASS") 
    else: print("  ❌ FAIL (Need more classes)")

    # 2. Object Properties (Target: 7+)
    obj_props = list(onto.object_properties())
    print(f"\n🔗 Object Properties Count: {len(obj_props)} / 7")
    for p in obj_props:
        print(f"  - {p.name}")
        if p.is_functional_for: print(f"    [Functional]")
        if p.is_functional_for: print(f"    [Functional]")
        if InverseFunctionalProperty in p.is_a: print(f"    [Inverse Functional] ✅")
    
    if len(obj_props) >= 7: print("  ✅ PASS")
    else: print("  ❌ FAIL")

    # 3. Data Properties (Target: 7+)
    data_props = list(onto.data_properties())
    print(f"\n📝 Data Properties Count: {len(data_props)} / 7")
    for p in data_props:
        print(f"  - {p.name}")
    
    if len(data_props) >= 7: print("  ✅ PASS")
    else: print("  ❌ FAIL")

    # 4. Axioms Check (Heuristic)
    print("\n📐 Axioms Check:")
    # Check for defined classes (Union, Intersection, Complement)
    defined_classes = [c for c in classes if c.equivalent_to]
    print(f"  - Defined Classes (Complex Axioms): {len(defined_classes)}")
    for c in defined_classes:
        print(f"    - {c.name}: {c.equivalent_to}")

if __name__ == "__main__":
    audit_ontology("file:////Users/ahsansaleem/Desktop/krrfinalproject/ontology/space_exploration.owl")
