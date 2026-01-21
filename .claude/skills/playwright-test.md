---
description: "Writes E2E tests using Playwright MCP server"
globs: ["e2e/**/*.dart", "test/e2e/**/*.dart", "integration_test/**/*.dart"]
alwaysApply: false
---

# Skill: Playwright E2E Tests

Write reliable end-to-end tests using Playwright MCP server.

## Usage

When writing E2E tests with Playwright, follow these patterns for reliable, maintainable tests.

## MCP Server Commands

The Playwright MCP server provides these tools:

```
playwright_navigate    - Navigate to URL
playwright_click       - Click element
playwright_fill        - Fill form field
playwright_select      - Select dropdown option
playwright_hover       - Hover over element
playwright_screenshot  - Capture screenshot
playwright_get_text    - Get element text
playwright_evaluate    - Run JavaScript
```

---

## Selector Strategies

### Best Selectors (Most Reliable)

```dart
// Role-based (accessibility-first)
'role=button[name="Submit"]'
'role=textbox[name="Email"]'
'role=link[name="Home"]'
'role=heading[name="Welcome"]'
'role=checkbox[name="Remember me"]'

// Test IDs (stable, explicit)
'[data-testid="submit-button"]'
'[data-testid="user-avatar"]'

// Labels (accessible)
'label:has-text("Email")'
'[placeholder="Enter your email"]'

// Text content
'text=Sign In'
'text=/Welcome, \w+/'  // Regex
```

### Avoid (Brittle)

```dart
// 🔴 CSS classes (change frequently)
'.btn-primary'
'.MuiButton-root'

// 🔴 Complex CSS paths (structure changes)
'div > div > button'
'#app > main > section:nth-child(2) > button'

// 🔴 XPath (hard to read/maintain)
'//div[@class="container"]//button'
```

---

## Common Test Patterns

### Login Flow

```
1. Navigate to /login
2. Fill email field with "user@example.com"
3. Fill password field with "password123"
4. Click "Sign In" button
5. Wait for navigation to /dashboard
6. Verify welcome message visible
```

```dart
// Using MCP commands
await playwright_navigate(url: 'http://localhost:3000/login');
await playwright_fill(selector: '[data-testid="email"]', value: 'user@example.com');
await playwright_fill(selector: '[data-testid="password"]', value: 'password123');
await playwright_click(selector: 'role=button[name="Sign In"]');
// Verify dashboard loaded
final welcomeText = await playwright_get_text(selector: '[data-testid="welcome"]');
// Assert welcomeText contains "Welcome"
```

### Form Submission

```
1. Navigate to form page
2. Fill required fields
3. Select dropdown options
4. Check checkboxes
5. Submit form
6. Verify success message
```

```dart
await playwright_navigate(url: 'http://localhost:3000/contact');
await playwright_fill(selector: 'role=textbox[name="Name"]', value: 'John Doe');
await playwright_fill(selector: 'role=textbox[name="Email"]', value: 'john@example.com');
await playwright_select(selector: '[data-testid="subject"]', value: 'support');
await playwright_fill(selector: 'role=textbox[name="Message"]', value: 'Hello, I need help.');
await playwright_click(selector: 'role=checkbox[name="I agree"]');
await playwright_click(selector: 'role=button[name="Send"]');
// Verify success
final alert = await playwright_get_text(selector: 'role=alert');
```

### CRUD Operations

```dart
// CREATE
await playwright_navigate(url: 'http://localhost:3000/todos');
await playwright_fill(selector: '[data-testid="new-todo"]', value: 'Buy groceries');
await playwright_click(selector: 'role=button[name="Add"]');

// READ - Verify item exists
final todoText = await playwright_get_text(selector: '[data-testid="todo-item"]:has-text("Buy groceries")');

// UPDATE - Mark complete
await playwright_click(selector: '[data-testid="todo-item"]:has-text("Buy groceries") >> role=checkbox');

// DELETE
await playwright_click(selector: '[data-testid="todo-item"]:has-text("Buy groceries") >> role=button[name="Delete"]');
await playwright_click(selector: 'role=button[name="Confirm"]');
```

### Navigation Testing

```dart
await playwright_navigate(url: 'http://localhost:3000/');

// Click nav link
await playwright_click(selector: 'role=link[name="Products"]');
// Verify URL changed (check via screenshot or evaluate)

await playwright_click(selector: 'role=link[name="About"]');

// Test back navigation
await playwright_evaluate(script: 'window.history.back()');
```

### Modal/Dialog Testing

```dart
// Open modal
await playwright_click(selector: 'role=button[name="Open Settings"]');

// Interact with modal content
await playwright_fill(selector: 'role=dialog >> role=textbox[name="Username"]', value: 'newuser');

// Close modal
await playwright_click(selector: 'role=dialog >> role=button[name="Save"]');

// Verify modal closed
// (modal should not be visible)
```

### Dropdown/Select Testing

```dart
// Standard select
await playwright_select(selector: '[data-testid="country-select"]', value: 'US');

// Custom dropdown (click to open, then select option)
await playwright_click(selector: '[data-testid="custom-dropdown"]');
await playwright_click(selector: 'role=option[name="United States"]');
```

### File Upload

```dart
// Via JavaScript evaluation
await playwright_evaluate(script: '''
  const input = document.querySelector('[data-testid="file-input"]');
  const dataTransfer = new DataTransfer();
  const file = new File(['test content'], 'test.txt', { type: 'text/plain' });
  dataTransfer.items.add(file);
  input.files = dataTransfer.files;
  input.dispatchEvent(new Event('change', { bubbles: true }));
''');
```

---

## Waiting Strategies

### Wait for Element

```dart
// Playwright auto-waits for elements, but you can be explicit
await playwright_evaluate(script: '''
  await page.waitForSelector('[data-testid="loading"]', { state: 'hidden' });
''');
```

### Wait for Navigation

```dart
await playwright_click(selector: 'role=button[name="Submit"]');
// Navigation happens automatically, verify with screenshot or URL check
await playwright_screenshot(name: 'after-submit');
```

### Wait for Network

```dart
// Wait for API response via evaluate
await playwright_evaluate(script: '''
  await Promise.all([
    page.waitForResponse('**/api/users'),
    page.click('[data-testid="load-users"]')
  ]);
''');
```

---

## Error Handling

### Check Element State

```dart
// Check if element exists before interacting
final exists = await playwright_evaluate(script: '''
  document.querySelector('[data-testid="error-message"]') !== null
''');

if (exists) {
  final errorText = await playwright_get_text(selector: '[data-testid="error-message"]');
  // Handle error...
}
```

### Retry Pattern

```dart
// Retry logic for flaky operations
for (int attempt = 0; attempt < 3; attempt++) {
  try {
    await playwright_click(selector: '[data-testid="submit"]');
    break;
  } catch (e) {
    if (attempt == 2) rethrow;
    await Future.delayed(Duration(seconds: 1));
  }
}
```

---

## Screenshots

### Capture for Debugging

```dart
// Capture current state
await playwright_screenshot(name: 'step-1-login-page');

// After action
await playwright_click(selector: 'role=button[name="Submit"]');
await playwright_screenshot(name: 'step-2-after-submit');
```

### Capture on Failure

```dart
try {
  await runTest();
} catch (e) {
  await playwright_screenshot(name: 'failure-${DateTime.now().millisecondsSinceEpoch}');
  rethrow;
}
```

---

## Test Data

### Test User Credentials

```dart
const testUsers = {
  'standard': {
    'email': 'test@example.com',
    'password': 'TestPass123!',
  },
  'admin': {
    'email': 'admin@example.com',
    'password': 'AdminPass123!',
  },
};
```

### Generate Unique Data

```dart
final uniqueEmail = 'test-${DateTime.now().millisecondsSinceEpoch}@example.com';
final uniqueName = 'Test User ${DateTime.now().millisecondsSinceEpoch}';
```

---

## Checklist

### Before Writing Test
- [ ] Identify the user journey being tested
- [ ] Determine required test data
- [ ] Add data-testid attributes to elements if missing
- [ ] Identify any async operations that need handling

### Writing Test
- [ ] Use stable selectors (role, testid, label)
- [ ] Handle loading states
- [ ] Add meaningful assertions
- [ ] Capture screenshots at key steps

### After Test
- [ ] Test passes consistently (not flaky)
- [ ] Test is independent (no shared state)
- [ ] Test cleans up after itself
- [ ] Test has descriptive name

---

## Quick Reference

| Action | Selector Example |
|--------|------------------|
| Click button | `role=button[name="Submit"]` |
| Fill input | `role=textbox[name="Email"]` |
| Check checkbox | `role=checkbox[name="Agree"]` |
| Select option | `role=combobox >> role=option[name="US"]` |
| Click link | `role=link[name="Home"]` |
| Find by test ID | `[data-testid="user-card"]` |
| Find by text | `text=Welcome back` |
| Find in container | `[data-testid="modal"] >> role=button` |
