# ChargeWise AI - Defect Logs & Bug Reports

> **Document Type:** Quality Assurance Defect Registry  
> **Classification:** SDET Defect Tracking & Root Cause Analysis  
> **Status:** Active  

---

## 1. Defect Summary Dashboard

| Bug ID | Module | Severity | Priority | Defect Title | Status | Environment |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `BUG-CW-001` | Booking API | High | High | Concurrent booking lock acquisition timeout returns 200 OK instead of 409 Conflict | Open | Staging/Local |
| `BUG-CW-002` | Station Discovery | Medium | Medium | Missing input sanitization on radiusKm allows negative values | In Review | Dev/Local |
| `BUG-CW-003` | UI BottomSheet | Medium | Low | Stale element reference when rapid switching between station cards | Fixed | Local UI |
| `BUG-CW-004` | ML Prediction | Low | Low | Peak hour demand prediction endpoint does not validate day boundaries (0-6) strictly | Open | ML Microservice |

---

## 2. Detailed Bug Reports

### BUG-CW-001: Concurrent booking lock acquisition returns 200 OK with success:false instead of HTTP 409 Conflict

- **Bug ID:** `BUG-CW-001`
- **Module:** Booking & Distributed Locking (`BookingController.java`)
- **Severity:** High (API Contract Inconsistency)
- **Priority:** High
- **Environment:** Localhost (Spring Boot 3.x, Port 8080)
- **Reported By:** QA Automation Engineer

#### Preconditions
1. Spring Boot backend and Redis running.
2. Station `st-001` exists with active chargers.

#### Steps to Reproduce
1. Dispatch `POST /api/v1/bookings/reserve` with body:
   ```json
   {
     "stationId": "st-001",
     "userPhone": "+91 98765 43210",
     "vehicleType": "EV Fleet Cab",
     "paymentMethod": "UPI"
   }
   ```
2. Trigger an artificial lock contention or timeout in `BookingService.java`.
3. Inspect HTTP response status code and body.

#### Expected Result
HTTP `409 Conflict` (or `423 Locked`) with payload:
```json
{
  "success": false,
  "error": "LOCK_ACQUISITION_TIMEOUT",
  "message": "Slot reserved by another driver."
}
```

#### Actual Result
HTTP `200 OK` is returned with JSON body `{"success": false, "passId": null, ...}`.

#### Root Cause Analysis
In `BookingController.java`:
```java
@PostMapping("/reserve")
public ResponseEntity<BookingResponse> reserveSlot(@RequestBody BookingRequest request) {
    BookingResponse response = bookingService.createAtomicReservation(request);
    return ResponseEntity.ok(response); // Always returns 200 OK regardless of response.isSuccess()
}
```

#### Suggested Fix
Return `ResponseEntity.status(HttpStatus.CONFLICT).body(response)` when `!response.isSuccess()`.

---

### BUG-CW-002: Missing validation on negative `radiusKm` in Station Discovery

- **Bug ID:** `BUG-CW-002`
- **Module:** Station Discovery (`StationController.java`)
- **Severity:** Medium
- **Priority:** Medium
- **Environment:** Backend API

#### Steps to Reproduce
1. Dispatch `GET /api/v1/stations/nearby?lat=13.0418&lng=80.2341&radiusKm=-50`
2. Observe backend query execution.

#### Expected Result
HTTP `400 Bad Request` with message: `"radiusKm must be a positive number greater than 0"`.

#### Actual Result
Request succeeds with HTTP `200 OK` and passes negative radius into geospatial query logic.

---

## 3. Standard Defect Report Template (For New Defects)

```markdown
### BUG-[PROJECT]-[NUMBER]: [Short Descriptive Title]

- **Bug ID:** BUG-CW-XXX
- **Module:** [Authentication / Station Discovery / Route Planning / Booking / DB / ML]
- **Severity:** [Blocker / Critical / Major / Minor / Trivial]
- **Priority:** [P1 - Urgent / P2 - High / P3 - Medium / P4 - Low]
- **Environment:** [OS / Browser / Backend Version / DB Version]
- **Reported By:** [Name]

#### Preconditions
- [List any required user state, database seed, or active flags]

#### Steps to Reproduce
1. [Step 1]
2. [Step 2]
3. [Step 3]

#### Expected Result
- [What should happen according to specification]

#### Actual Result
- [What actually happened]

#### Evidence & Attachments
- [Screenshots / HTTP Payloads / Console Logs]

#### Suggested Remediation
- [Technical fix recommendation or code pointer]
```
