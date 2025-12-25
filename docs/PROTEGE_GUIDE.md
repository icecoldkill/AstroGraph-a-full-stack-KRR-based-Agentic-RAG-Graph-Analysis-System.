# Protégé Setup Guide for KRR Project
## Fulfilling Rubric Requirements 5, 6, 9

This guide helps you use Protégé to meet the project requirements for:
- Ontology Visualization in Protégé/OWLVis
- Graph Generation and Validation in Protégé
- Reasoning Scenarios and Validation (Using Protégé)

---

## Step 1: Download and Install Protégé

1. Go to: https://protege.stanford.edu/
2. Download **Protégé Desktop** (free)
3. Install and open

---

## Step 2: Open the Ontology

1. File → Open
2. Navigate to: `/Users/ahsansaleem/Desktop/krrfinalproject/ontology/`
3. Open: `space_exploration.owl`

---

## Step 3: Screenshot - Ontology Classes (Requirement 5)

1. Click **"Entities"** tab
2. Click **"Classes"** sub-tab
3. Expand the class hierarchy
4. **Take screenshot** showing all classes

---

## Step 4: Screenshot - Object Properties

1. Click **"Object Properties"** sub-tab
2. Expand to show all properties
3. **Take screenshot**

---

## Step 5: Screenshot - Data Properties

1. Click **"Data Properties"** sub-tab
2. Expand to show all properties
3. **Take screenshot**

---

## Step 6: Run Reasoner (Requirements 6, 9)

### Start Reasoning:
1. Click **"Reasoner"** menu
2. Select **"HermiT"** or **"Pellet"**
3. Click **"Start reasoner"**

### Take Screenshots:
1. Reasoner running (with inferred hierarchy)
2. Any inconsistencies detected (or note "No inconsistencies")

---

## Step 7: View Individuals (A-Box)

1. Click **"Individuals by class"** tab
2. Select a class like `SpaceMission`
3. View the individuals
4. **Take screenshot**

---

## Step 8: Use OntoGraf Plugin (Visualization)

### Install OntoGraf:
1. File → Preferences → Plugins
2. Search for "OntoGraf"
3. Install and restart Protégé

### Visualize:
1. Window → Tabs → OntoGraf
2. Select classes to visualize
3. **Take screenshot** of the graph

---

## Alternative: OWLViz Plugin

1. Install OWLViz from Plugins
2. Window → Tabs → OWLViz
3. Start reasoner first
4. View class hierarchy as graph
5. **Take screenshot**

---

## Screenshots Checklist for Report

| Screenshot | Tab in Protégé |
|------------|----------------|
| Class Hierarchy | Entities → Classes |
| Object Properties | Entities → Object Properties |
| Data Properties | Entities → Data Properties |
| Reasoner Running | Reasoner → HermiT → Started |
| Inferred Hierarchy | After reasoning |
| Individuals/Instances | Individuals by class |
| Visual Graph (OntoGraf) | Window → Tabs → OntoGraf |

---

## Reasoning Scenarios to Demonstrate

1. **Classification**: Show how HermiT infers class memberships
2. **Consistency Check**: Demonstrate no logical contradictions
3. **Property Domains/Ranges**: Show inferred property restrictions

---

## Files to Use

- **Ontology (T-Box)**: `ontology/space_exploration.owl`
- **With Individuals (A-Box)**: Import `data/space_data.rdf` into Protégé
  - File → Merge Ontology → Select space_data.rdf
