# RFC: URL Shortener Service (Phase 1)

## 1. Goal
Build a high-performance REST API that accepts long URLs and returns short, shareable links, tracking usage analytics.

## 2. API Endpoints

### Endpoint A: Create Short Link
* **URL:** `/url`
* **Method:** `POST`
* **Request Body (JSON):**
    ```json
    {
      "target_url": "[https://www.wikipedia.org/wiki/System_design](https://www.wikipedia.org/wiki/System_design)"
    }
    ```
* **Success Response (201 Created):**
    ```json
    {
      "key": "aZb12",
      "short_url": "http://localhost:8000/aZb12",
      "target_url": "[https://www.wikipedia.org/wiki/System_design](https://www.wikipedia.org/wiki/System_design)"
    }
    ```

### Endpoint B: Redirect to Original
* **URL:** `/{key}` (e.g., `/aZb12`)
* **Method:** `GET`
* **Behavior:**
    * Find the `target_url` associated with the `key`.
    * Increment the `clicks` counter in the database.
    * Return HTTP `302 Found` (Temporary Redirect).
    * Set header `Location: {target_url}`.

### Endpoint C: Get Stats (Optional for V1)
* **URL:** `/url/{key}`
* **Method:** `GET`
* **Success Response:**
    ```json
    {
      "key": "aZb12",
      "clicks": 5,
      "url": "[https://www.wikipedia.org/wiki/System_design](https://www.wikipedia.org/wiki/System_design)"
    }
    ```

## 3. Database Schema (SQLite)

**Table Name:** `urls`

| Column Name | Data Type | Purpose |
| :--- | :--- | :--- |
| `id` | Integer (PK) | Unique ID for the database row. |
| `key` | String (Unique) | The generated short code (e.g., "aZb12"). Indexed for fast search. |
| `target_url` | String | The original long URL. |
| `is_active` | Boolean | To soft-delete links without removing data. Default: `True`. |
| `clicks` | Integer | Analytics counter. Default: `0`. |

## 4. Algorithm Strategy (Phase 1)
**Strategy:** Random String Generation.
* **Logic:** Generate a random 5-character string using `a-z`, `A-Z`, `0-9`.
* **Collision Handling:** (Naive approach for Phase 1) Query the DB. If the key exists, generate a new one and try again.