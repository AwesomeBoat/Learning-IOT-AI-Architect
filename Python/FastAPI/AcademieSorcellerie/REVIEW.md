# Code Review — Académie de Sorcellerie API

> Review date: 2026-08-20 · Day 3 of learning FastAPI
> All findings below were confirmed by running the app against a `TestClient`.
> Security (hashing, JWT, etc.) is intentionally out of scope — it's the next learning step.

---

## ✅ What's good

- **Structure matches the spec**: `models/` + `controllers/` + centralised `database.py`, one `APIRouter` per domain with `prefix` and `tags`.
- **`find_X_or_404` helpers** — the lookup + raise is factored into one function instead of being repeated in 5 endpoints.
- **Three-model pattern** (`House` / `HouseCreate` / `HouseUpdate`) — this is the idiomatic FastAPI split.
- **`exclude_unset=True` on PATCH** — the difference between PATCH and PUT is understood. Most commonly missed concept by beginners.
- **Explicit `status_code=` on POST/DELETE**, `Field(ge=1, le=7)`, `Literal[...]` for enums — good Pydantic v2 usage.
- Seed data is complete and clean; `.gitignore` is correct (no `__pycache__` tracked).

---

## 🐛 Bugs

### [ ] Bug 1 — `PATCH /user/update_user/{id}` is broken for every student and teacher user

**File:** `controllers/user.py:128-140`
**Severity:** High — endpoint is unusable for 4 of the 5 seeded users.

`UserUpdate` gives every field a default, so `data.model_dump()` **always** returns all 5 keys.
That makes the `if key not in dump_data` check at line 133 dead code that never fires, and
`student_id` / `teacher_id` get forced to `None` on every patch.

```
PATCH /user/update_user/2  {"email": "new@x.fr"}
→ 400 {'detail': {'error': 'data is not valid'}}
```

**Fix:** start from the stored user and overlay only the fields actually sent.

```python
dump_data = {**user, **data.model_dump(exclude_unset=True)}
```

The two `for` loops and the `keys_set_null` / `keys_no_change` lists can then be deleted.

---

### [ ] Bug 2 — Malformed route: missing `/`

**File:** `controllers/house.py:50`
**Severity:** Medium — the endpoint is unreachable at its intended URL.

```python
@router.patch("/update_house{house_id}")   # → PATCH /house/update_house3
```

**Fix:** `@router.patch("/update_house/{house_id}")`

---

### [ ] Bug 3 — `POST /user/login` takes credentials as query params, not a body

**File:** `controllers/user.py:62`
**Severity:** High — spec violation + password leaks into URLs and access logs.

Bare `email: str, password: str` on a POST become **query parameters**. Sending a JSON body
returns 422. The spec says *"Reçoit email + mot de passe"*.

```
POST /user/login  {"email": "...", "password": "..."}   → 422 Unprocessable Entity
POST /user/login?email=...&password=...                 → 200 OK
```

**Fix:** you already started `models/login.py` — wire it up as the body parameter.

```python
# models/login.py
class Login(BaseModel):
    email: EmailStr
    password: str

# controllers/user.py
@router.post("/login")
def login(credentials: Login): ...
```

---

### [ ] Bug 4 — `login` can return `null` with a 200, and returns an incomplete payload

**File:** `controllers/user.py:69-80`
**Severity:** Medium

Three `if`s with no `else`: if `role` ever falls outside them the function returns `None` → `200 null`.
Also the spec asks to return **the user**, its role *and* the linked id — only the role is returned.

**Fix:** build one response object and return it once, with a `LoginResponse` response model.

---

### [ ] Bug 5 — `PUT /subject/create_subject/{id}` returns an object with no `id`

**File:** `controllers/subject.py:61`
**Severity:** Medium

Returns `new_subject` (the raw payload dump) instead of `subject` (the updated record).

```
PUT /subject/create_subject/1 → 200 {'title': 'X', ...}   ← id is gone
```

**Fix:** `return subject`

---

### [ ] Bug 6 — `PATCH /subject/update_subject/{id}` returns only the diff, with the wrong status

**File:** `controllers/subject.py:65-75`
**Severity:** Medium — inconsistent with the 3 other routers, which do this correctly.

Returns `new_data_dict` (`{'max_capacity': 99}`) instead of the full resource, and `202 ACCEPTED`
means "queued for later processing" — the update is synchronous here.

**Fix:** `status_code=status.HTTP_200_OK` and `return subject`.

---

### [ ] Bug 7 — `DELETE /user/delete_user` takes `user_id` as a query param

**File:** `controllers/user.py:156`
**Severity:** Low — inconsistent with the other 4 resources, which all use `/{id}` in the path.

**Fix:** `@router.delete("/delete_user/{user_id}", ...)`

---

### [ ] Bug 8 — Foreign keys are never validated

**Files:** `controllers/student.py` (POST, PUT, PATCH), `controllers/subject.py` (POST, PUT, PATCH)
**Severity:** Medium — lets the mock DB drift into an inconsistent state.

```
POST  /student/create_student  {"house_id": 999, ...}  → 201 Created
PATCH /student/update_student/1 {"house_id": 999}      → 200 OK
```

Same for `Subject.teacher_id`. The helpers already exist — they just aren't called.

**Fix:** `find_house_or_404(student_data.house_id)` before writing (guard for `None` on PATCH).

---

## ⚠️ Design issues

### [ ] Issue 9 — Passwords are returned in plaintext by the API

**File:** `controllers/user.py:13-28`, `models/user.py`
**Severity:** High — not a "security later" item, it's a missing response model.

```
GET /user/get_user → [{'id': 1, 'email': '...', 'password': 'admin123', ...}]
```

**Fix:** add a `UserPublic` model without the password field and use it as `response_model`.

```python
class UserPublic(BaseModel):
    id: int
    email: EmailStr
    role: Literal["student", "teacher", "admin"]
    student_id: int | None = None
    teacher_id: int | None = None

@router.get("/get_user", response_model=list[UserPublic])
```

---

### [ ] Issue 10 — No `response_model=` anywhere

**Files:** all 5 controllers
**Severity:** High — the biggest thing missing overall.

Swagger currently shows every response as an empty `{}`, nothing is validated on the way out,
and the `-> dict` annotations do nothing.

**Fix:** add `response_model=House` / `response_model=list[House]` to every route.
You get output validation, field filtering and real docs for free.

---

### [ ] Issue 11 — Star imports everywhere

**Files:** all 5 controllers, `main.py:3`
**Severity:** Medium — hides a dependency that will break silently.

`from database import *` + `from models.x import *`. This is why `status` works in
`controllers/student.py:28` despite never being imported there — it leaks in through
`database.py`'s own `from fastapi import HTTPException, status`.

**Fix:** be explicit.

```python
from fastapi import APIRouter, status
from database import students, find_student_or_404, generate_id
from models.student import Student, StudentCreate, StudentUpdate
```

Also: the `from database import *` in `main.py:3` is entirely unused — delete it.

---

### [ ] Issue 12 — RPC-style URLs instead of REST

**Files:** all 5 controllers
**Severity:** Medium — worth fixing now, while there are only 5 routers.

The HTTP verb already states the action; repeating it in the path is redundant.
The convention is a **plural noun**.

| Current | REST |
|---|---|
| `GET /house/get_house` | `GET /houses` |
| `GET /house/get_house/{id}` | `GET /houses/{id}` |
| `POST /house/create_house` | `POST /houses` |
| `PATCH /house/update_house/{id}` | `PATCH /houses/{id}` |
| `DELETE /house/delete_house/{id}` | `DELETE /houses/{id}` |

Set `prefix="/houses"` and the paths become `""` and `"/{house_id}"`.
This also removes the odd `PUT /student/create_student/{id}` — a PUT on a route named "create".

---

### [ ] Issue 13 — `generate_id` is over-engineered and raises the wrong error type

**File:** `database.py:99-114`
**Severity:** Low

Checks membership in a hardcoded `lists`, and raises **HTTP 404** for what would be a *programmer*
bug. A 404 tells the client "your resource doesn't exist" — which would be a lie here.

**Fix:**

```python
def generate_id(items: list[dict]) -> int:
    return max((item["id"] for item in items), default=0) + 1
```

Also: `controllers/house.py:36-39` inlines this logic instead of calling the helper — use
`generate_id(houses)` there too.

---

### [ ] Issue 14 — `check_if_user_data_is_valid` belongs in the model

**File:** `database.py:151-217`
**Severity:** Medium

Returns `0`/`1` instead of `bool`, and accepts `dict | UserCreate`, which forces the `isinstance`
dance at line 172. In Pydantic v2 these ~60 lines are a `@model_validator`:

```python
@model_validator(mode="after")
def check_role_consistency(self):
    expected = {"student": ("student_id", "teacher_id"),
                "teacher": ("teacher_id", "student_id")}
    if self.role == "admin":
        if self.student_id or self.teacher_id:
            raise ValueError("admin must not have student_id or teacher_id")
    else:
        required, forbidden = expected[self.role]
        if getattr(self, required) is None or getattr(self, forbidden) is not None:
            raise ValueError(f"{self.role} requires {required} only")
    return self
```

Validation belongs in the model, not in `database.py`.

---

### [ ] Issue 15 — Minor typing gaps

**Files:** `models/*.py`
**Severity:** Low

- `models/house.py` — `values: list` → `list[str]`
- `models/user.py` — `email: str` → `EmailStr` (needs `pip install "pydantic[email]"`)
- `models/student.py` — `StudentCreate.status` should default to `"active"` rather than be required
- `models/house.py` — `HouseUpdate` is missing `founder` (deliberate? then fine — just be consistent)

---

### [ ] Issue 16 — `detail={"error": "..."}` is non-idiomatic

**Files:** `database.py`, `controllers/user.py`
**Severity:** Low

FastAPI's convention is `detail="house not found"` (a string). Nesting a dict forces clients to
read `detail.error`. Not wrong — just pick one style and apply it everywhere.

---

## 📋 Spec coverage

Day 1 (*Fondations et comptes*) is done, minus the items below.

| Requirement | Status |
|---|---|
| CRUD Maison / Professeur / Cours / Élève | ✅ (`House` has no PUT — minor) |
| `POST /login` | ⚠️ Bugs 3 & 4 |
| **`X-User-Id` header + `HTTPException(401)`** | ❌ **not started — next task** |
| Seed data (4 maisons, ~10 élèves, profs, cours, comptes) | ✅ |
| Inscription / Examen / Résultat | ❌ Day 2 |
| Compétences / Maîtrise / Tournois | ❌ Day 3 |
| `POST /academie/cloturer-annee` | ❌ Day 4 |

For `X-User-Id`, the tool you want is a **dependency** — written once, reused on every protected route:

```python
# dependencies.py
from fastapi import Header, HTTPException, status

def get_current_user(x_user_id: int | None = Header(default=None)) -> dict:
    if x_user_id is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "X-User-Id header required")
    return find_user_or_404(x_user_id)

# usage
@router.get("/me/cours")
def my_courses(user: dict = Depends(get_current_user)): ...
```

---

## 🔧 Suggested order

1. **Bugs 1, 2, 5, 6** — outright broken behaviour (~15 min).
2. **Issues 9 + 10** — `response_model` everywhere + `UserPublic`. Biggest learning payoff, kills the password leak.
3. **Bugs 3, 4** + the `X-User-Id` dependency — unblocks the rest of the spec.
4. **Issue 12** — rename routes to REST plural, while it's still cheap.
5. **Issues 11, 14** — explicit imports, move user validation into the model.
6. **Bugs 7, 8** and **Issues 13, 15, 16** — cleanup pass.
