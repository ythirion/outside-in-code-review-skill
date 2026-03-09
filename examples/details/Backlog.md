# 📦 Product Backlog — jurassic-code
> ⚠️ AI-inferred from code — validate with product owners before use

← [Back to Report](../Report.md)

---

## Domain: Zone Management

### Feature 1 — Create a Park Zone

**User Story**
> As a **park operations manager**, I want to **create a new zone** so that I can **organize dinosaurs into separate managed areas**.

**Acceptance Criteria**

```gherkin
Scenario: Successfully create an open zone
  Given the park has no zone named "Ismaloya Mountains"
  When I create a zone with name "Ismaloya Mountains" and status Open
  Then the zone appears in the list of all zones
  And the zone status is "Open"

Scenario: Reject duplicate zone creation
  Given a zone named "Western Ridge" already exists
  When I try to create another zone with name "Western Ridge"
  Then an error "Zone already exists." is returned
  And the zone list still contains only one "Western Ridge"
```

**Examples**
| Zone Name | IsOpen | Expected |
|-----------|--------|----------|
| "Main Temple" | true | Created successfully |
| "Western Ridge" | true | Error — already exists |
| "Quarantine" | false | Created as closed zone |

---

### Feature 2 — Open / Close a Zone (Toggle)

**User Story**
> As a **park safety officer**, I want to **toggle a zone between open and closed** so that I can **restrict dinosaur movement during incidents**.

**Acceptance Criteria**

```gherkin
Scenario: Toggle an open zone to closed
  Given a zone "Western Ridge" is Open
  When I toggle zone "Western Ridge"
  Then zone "Western Ridge" status becomes Closed

Scenario: Toggle a closed zone to open
  Given a zone "Eastern Ridge" is Closed
  When I toggle zone "Eastern Ridge"
  Then zone "Eastern Ridge" status becomes Open
```

**Examples**
| Zone Name | Initial Status | After Toggle |
|-----------|---------------|--------------|
| "Western Ridge" | Open | Closed |
| "Eastern Ridge" | Closed | Open |

---

### Feature 3 — List All Zones

**User Story**
> As a **park ranger**, I want to **view all zones and their current dinosaur populations** so that I can **monitor the park at a glance**.

**Acceptance Criteria**

```gherkin
Scenario: Retrieve all zones with dinosaur counts
  Given zones "Ismaloya Mountains", "Western Ridge", "Eastern Ridge" exist
  And each zone has at least one dinosaur
  When I request all zones
  Then I receive a list of 3 zones
  And each zone includes its name, open/closed status, and list of dinosaurs
```

---

## Domain: Dinosaur Management

### Feature 4 — Add a Dinosaur to a Zone

**User Story**
> As a **park keeper**, I want to **assign a dinosaur to an open zone** so that I can **track where each animal lives**.

**Acceptance Criteria**

```gherkin
Scenario: Successfully add a dinosaur to an open zone
  Given zone "Ismaloya Mountains" is Open
  When I add dinosaur "Rexy" (T-Rex, carnivorous) to "Ismaloya Mountains"
  Then "Rexy" appears in the dinosaur list for "Ismaloya Mountains"

Scenario: Reject adding a dinosaur to a closed zone
  Given zone "Quarantine" is Closed
  When I try to add dinosaur "Stego" to "Quarantine"
  Then an error "Zone is closed or does not exist." is returned

Scenario: Reject adding a dinosaur to a non-existent zone
  Given no zone named "Atlantis" exists
  When I try to add dinosaur "Dino" to "Atlantis"
  Then an error "Zone is closed or does not exist." is returned
```

**Examples**
| Dinosaur | Zone | Zone Status | Expected |
|----------|------|-------------|----------|
| "Rexy" (T-Rex) | "Ismaloya Mountains" | Open | Added |
| "Stego" | "Quarantine" | Closed | Error |
| "Dino" | "Atlantis" | Missing | Error |

---

### Feature 5 — Move a Dinosaur Between Zones

**User Story**
> As a **park keeper**, I want to **move a dinosaur from one zone to another open zone** so that I can **respond to safety or habitat needs**.

**Acceptance Criteria**

```gherkin
Scenario: Successfully move a dinosaur to an open zone
  Given dinosaur "TestDino1" is in zone "Test Zone 1" (Open)
  And zone "Test Zone 2" is Open
  When I move "TestDino1" from "Test Zone 1" to "Test Zone 2"
  Then "TestDino1" appears in "Test Zone 2"
  And "TestDino1" is no longer in "Test Zone 1"

Scenario: Reject moving a dinosaur to a closed zone
  Given dinosaur "TestDino1" is in zone "Test Zone 1"
  And zone "Test Zone 2" is Closed
  When I try to move "TestDino1" to "Test Zone 2"
  Then an error "Zones are closed or do not exist." is returned

Scenario: Reject moving a dinosaur to a non-existent zone
  Given dinosaur "DinoC" is in zone "Test Zone 3"
  When I try to move "DinoC" to "Non-Existent Zone"
  Then an error "Zones are closed or do not exist." is returned
```

---

### Feature 6 — List Dinosaurs in a Zone

**User Story**
> As a **park ranger**, I want to **view all dinosaurs in a specific zone** so that I can **verify zone population and health status**.

**Acceptance Criteria**

```gherkin
Scenario: Retrieve dinosaurs from an existing zone
  Given zone "Ismaloya Mountains" contains "Rexy", "Bucky", "Echo"
  When I request dinosaurs in "Ismaloya Mountains"
  Then I receive a list of 3 dinosaurs
  And each dinosaur shows name, species, carnivore flag, sick flag, and last fed time

Scenario: Error on non-existent zone
  Given no zone "Ghost Zone" exists
  When I request dinosaurs in "Ghost Zone"
  Then an error "Zone does not exist." is returned
```

---

## Domain: Safety / Compatibility ⚠️

### Feature 7 — Check Species Coexistence ⚠️

> ⚠️ **Incomplete feature** — logic is hardcoded for 3 species only (T-Rex, Velociraptor, Triceratops). All other species pairs return `true` by default with no validation.

**User Story**
> As a **park safety officer**, I want to **check whether two species can safely coexist in the same zone** so that I can **prevent animal attacks**.

**Acceptance Criteria**

```gherkin
Scenario: T-Rex cannot coexist with any other species
  Given species "T-Rex" and "Velociraptor"
  When I check coexistence
  Then the result is false (incompatible)

Scenario: Triceratops can coexist with Velociraptor
  Given species "Triceratops" and "Velociraptor"
  When I check coexistence
  Then the result is true (compatible)

Scenario: Unknown species pair defaults to compatible (bug/gap)
  Given species "Brachiosaurus" and "Stegosaurus"
  When I check coexistence
  Then the result is true
  # NOTE: this is a gap — no domain logic covers herbivore-herbivore validation
```

**Examples**
| Species 1 | Species 2 | Expected | Covered by Test? |
|-----------|-----------|----------|-----------------|
| T-Rex | Velociraptor | false | ✅ |
| Triceratops | Velociraptor | true | ✅ |
| Brachiosaurus | Stegosaurus | true (default) | ❌ |
| T-Rex | Triceratops | false | ❌ |

---

## Domain: Health Monitoring ⚠️

### Feature 8 — Track Sick Dinosaurs ⚠️

> ⚠️ **Inferred but untested** — `IsSick` and `HealthStatus` fields exist in the model and are mapped through the data layer, but no dedicated endpoint, alert, or business rule acts on sick status. This feature appears partially implemented.

**User Story**
> As a **park veterinarian**, I want to **identify sick dinosaurs** so that I can **prioritize medical interventions**.

**Acceptance Criteria**

```gherkin
Scenario: Sick dinosaur is flagged in zone listing
  Given dinosaur "Charlie" (Velociraptor, IsSick=true) is in "Western Ridge"
  When I retrieve dinosaurs in "Western Ridge"
  Then "Charlie" appears with IsSick = true
```

---

## Domain: Feeding Tracking ⚠️

### Feature 9 — Track Last Feeding Time ⚠️

> ⚠️ **Inferred but untested** — `LastFed` / `FeedingTime` is stored and mapped but no feeding endpoint, alert threshold, or business rule uses this data.

**User Story**
> As a **park keeper**, I want to **see when each dinosaur was last fed** so that I can **schedule feeding rounds**.

**Acceptance Criteria**

```gherkin
Scenario: Feeding time is preserved across persistence
  Given dinosaur "Charlie" was last fed yesterday
  When I retrieve dinosaurs in "Western Ridge"
  Then "Charlie" shows LastFed = yesterday's date
```
