# Layout Redesign - React to Streamlit Adaptation

## Overview
This document outlines the plan to adapt the React-based Test Case Manager layout to our Streamlit Test Case Documentation Tool. The goal is to create a modern, clean, and user-friendly interface that matches the visual design of the React components.

## Repository
**Remote**: https://github.com/louisgarnier/Documentation.git

---

## Design Reference

### React Component Structure
- **App.tsx**: Main layout with header, main content, and conditional footer
- **Header**: Sticky header with title and subtitle
- **TestCaseList**: Container for test case items with spacing
- **TestCaseItem**: Individual test case card with checkbox, content, and status badge
- **TestCaseDetail**: Detail view with back button and information grid
- **Footer**: Conditional footer with export functionality

---

## 1. Header Component

### Current State
- Simple title in Streamlit sidebar or main area

### Target Design
- **Sticky header** at the top of the page
- **Title**: "Test Case Manager" (or "Test Case Documentation Tool")
- **Subtitle**: "Review, select, and manage your test cases with ease."
- **Styling**:
  - Background: `bg-surface/50` with backdrop blur
  - Border bottom: `border-muted/50`
  - Padding: `py-6 px-4 sm:px-6 lg:p-8`
  - Max width: `max-w-7xl` centered
  - Sticky positioning: `sticky top-0 z-10`

### Streamlit Implementation
- Use `st.container()` with custom CSS
- Apply sticky positioning via CSS
- Use `st.markdown()` for title and subtitle
- Center content with max-width constraint

### CSS Requirements
```css
.header-container {
  position: sticky;
  top: 0;
  z-index: 10;
  background-color: rgba(/* surface color with 50% opacity */);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid /* muted color */;
  padding: 1.5rem 1rem;
}

@media (min-width: 640px) {
  .header-container {
    padding: 1.5rem 1.5rem;
  }
}

@media (min-width: 1024px) {
  .header-container {
    padding: 2rem 2rem;
  }
}
```

---

## 2. Test Case List Page

### Current State
- Table-style layout with columns
- Checkboxes in first column
- Clickable rows

### Target Design
- **Card-based layout** instead of table
- **Vertical spacing**: `space-y-4` between cards
- **Responsive padding**: `p-4 sm:p-6 lg:p-8`
- **Max width**: `max-w-7xl` centered

### Streamlit Implementation
- Replace table layout with card containers
- Use `st.container()` for each test case card
- Apply custom CSS for card styling
- Use columns for responsive layout

---

## 3. Test Case Item (Card)

### Current State
- Table row with multiple columns
- Checkbox, test number, description, date, delete button

### Target Design

#### Layout Structure
```
┌─────────────────────────────────────────────────────┐
│ [✓] │ Test Number (Bold)        │ [Status Badge] │
│     │ Description text...                            │
│     │ Created: Date                                  │
└─────────────────────────────────────────────────────┘
```

#### Components

1. **Custom Checkbox** (Left)
   - Square box with rounded corners
   - Checkmark icon when selected
   - Border color changes on selection
   - Background color on selection
   - Click stops propagation (doesn't trigger card click)

2. **Content Area** (Center, flex-grow)
   - **Test Number**: Bold, large text (`font-bold text-lg`)
   - **Description**: Secondary text color
   - **Created Date**: Small text, muted color

3. **Status Badge** (Right)
   - Rounded pill shape (`rounded-full`)
   - Color-coded:
     - Pass: Green (`bg-green-500/20 text-green-300`)
     - Fail: Red (`bg-red-500/20 text-red-300`)
     - Untested: Yellow (`bg-yellow-500/20 text-yellow-300`)
   - Small padding (`px-2 py-1 text-xs font-bold`)

#### Visual Effects
- **Hover State**:
  - Shadow enhancement: `hover:shadow-primary/20`
  - Ring effect: `hover:ring-2 hover:ring-primary/50`
  - Transition: `transition-all duration-200`
- **Card Styling**:
  - Background: `bg-surface`
  - Shadow: `shadow-lg`
  - Rounded corners: `rounded-lg`
  - Padding: `p-4`
  - Cursor: `cursor-pointer`

### Streamlit Implementation

#### HTML Structure
```html
<div class="test-case-card" onclick="handleCardClick(id)">
  <div class="checkbox-container" onclick="handleCheckboxClick(id, event)">
    <div class="custom-checkbox" data-selected="true/false">
      <!-- Checkmark icon if selected -->
    </div>
  </div>
  <div class="card-content">
    <div class="card-header">
      <h3 class="test-number">TC001</h3>
      <span class="status-badge status-pass">Pass</span>
    </div>
    <p class="description">Test case description...</p>
    <p class="created-date">Created: January 15, 2024</p>
  </div>
</div>
```

#### CSS Requirements
```css
.test-case-card {
  background-color: /* surface color */;
  border-radius: 0.5rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  padding: 1rem;
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  cursor: pointer;
  transition: all 0.2s;
  margin-bottom: 1rem;
}

.test-case-card:hover {
  box-shadow: 0 10px 15px -3px rgba(/* primary color with 20% opacity */);
  outline: 2px solid rgba(/* primary color with 50% opacity */);
}

.custom-checkbox {
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 0.375rem;
  border: 2px solid /* border color */;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.2s;
}

.custom-checkbox[data-selected="true"] {
  background-color: /* primary color */;
  border-color: /* primary color */;
}

.status-badge {
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
  font-weight: bold;
  border-radius: 9999px;
  display: inline-block;
}

.status-badge.status-pass {
  background-color: rgba(34, 197, 94, 0.2);
  color: rgb(134, 239, 172);
}

.status-badge.status-fail {
  background-color: rgba(239, 68, 68, 0.2);
  color: rgb(252, 165, 165);
}

.status-badge.status-untested {
  background-color: rgba(234, 179, 8, 0.2);
  color: rgb(253, 224, 71);
}
```

#### JavaScript Requirements
- Handle checkbox click (stop propagation)
- Handle card click (navigate to detail)
- Update checkbox state visually

---

## 4. Test Case Detail Page

### Current State
- Form-based layout with editable fields
- Steps in expandable sections

### Target Design

#### Layout Structure
```
┌─────────────────────────────────────────────────────┐
│ ← Back to List                                       │
│                                                      │
│ ┌─────────────────────────────────────────────────┐ │
│ │ Test Number (Large)        │ [Status Badge] │ │
│ │ Description                                      │ │
│ ├─────────────────────────────────────────────────┤ │
│ │ Test Steps          │ Expected Result           │ │
│ │ 1. Step one         │ Result description...     │ │
│ │ 2. Step two         │                           │ │
│ │                     │ Details                   │ │
│ │                     │ Created: Date             │ │
│ └─────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

#### Components

1. **Back Button** (Top Left)
   - Icon: Chevron left
   - Text: "Back to List"
   - Styling: Primary color, hover effect
   - Font: Semibold

2. **Detail Card**
   - Background: `bg-surface`
   - Shadow: `shadow-lg`
   - Rounded: `rounded-lg`
   - Padding: `p-6`

3. **Header Section**
   - Flex layout: row on desktop, column on mobile
   - Left: Test number (large, bold) + description
   - Right: Status badge
   - Border bottom separator

4. **Content Grid** (2 columns on desktop, 1 on mobile)
   - **Left Column**: Test Steps (ordered list)
   - **Right Column**: Expected Result + Details

### Streamlit Implementation
- Use `st.columns()` for grid layout
- Custom CSS for card styling
- Back button with navigation logic
- Maintain existing step editing functionality

---

## 5. Footer Component

### Current State
- Export button in main area or sidebar

### Target Design
- **Conditional**: Only visible on list view
- **Content**:
  - Selected count display
  - Export button
- **Positioning**: Fixed or sticky at bottom
- **Styling**: Similar to header (surface background, border top)

### Streamlit Implementation
- Use conditional rendering based on `current_view`
- Display selected count
- Export button with existing functionality

---

## 6. Color Scheme

### Colors to Define
- **Background**: Base background color
- **Surface**: Card/container background
- **Text**: Primary text color
- **Text Secondary**: Secondary text color
- **Muted**: Muted text and borders
- **Primary**: Primary accent color
- **Green**: Pass status (with opacity variants)
- **Red**: Fail status (with opacity variants)
- **Yellow**: Untested status (with opacity variants)

### Implementation
- Use CSS variables or direct color values
- Apply opacity using `rgba()` or CSS opacity

---

## 7. Responsive Design

### Breakpoints
- **sm**: 640px
- **md**: 768px
- **lg**: 1024px

### Adaptations
- Padding adjustments per breakpoint
- Grid layout changes (2 columns → 1 column on mobile)
- Font size adjustments
- Spacing adjustments

---

## 8. Implementation Steps

### Phase 1: Header
1. Create header container with CSS
2. Add title and subtitle
3. Apply sticky positioning
4. Test responsiveness

### Phase 2: Test Case List Layout
1. Replace table with card containers
2. Apply spacing and padding
3. Center content with max-width
4. Test layout

### Phase 3: Test Case Card
1. Create card HTML structure
2. Implement custom checkbox
3. Add status badges
4. Apply hover effects
5. Implement click handlers
6. Test interactions

### Phase 4: Test Case Detail
1. Add back button
2. Restructure detail layout
3. Apply card styling
4. Implement grid layout
5. Test responsiveness

### Phase 5: Footer
1. Create footer component
2. Add conditional rendering
3. Display selected count
4. Style export button
5. Test functionality

### Phase 6: Polish
1. Refine colors and spacing
2. Test all interactions
3. Optimize performance
4. Cross-browser testing

---

## 9. Technical Considerations

### Streamlit Limitations
- Limited JavaScript interaction
- CSS injection via `st.markdown()` with `unsafe_allow_html=True`
- Session state for navigation
- No native component library

### Solutions
- Use `streamlit.components.v1.html()` for complex interactions if needed
- Leverage CSS for visual effects
- Use session state for state management
- Custom HTML/CSS/JS for checkbox and interactions

### Performance
- Minimize CSS size
- Use efficient selectors
- Avoid excessive DOM manipulation
- Cache styles where possible

---

## 10. Testing Checklist

- [ ] Header displays correctly and is sticky
- [ ] Test case cards render properly
- [ ] Checkbox selection works independently
- [ ] Card click navigates to detail view
- [ ] Status badges display with correct colors
- [ ] Hover effects work on cards
- [ ] Back button navigates correctly
- [ ] Detail view displays all information
- [ ] Footer shows correct selected count
- [ ] Export button works
- [ ] Responsive design works on mobile
- [ ] All interactions are smooth
- [ ] Colors match design reference
- [ ] Spacing is consistent

---

## Notes

- Maintain existing functionality (CRUD operations, Excel export)
- Preserve data structure and database schema
- Keep navigation logic intact
- Ensure accessibility where possible
- Document any custom CSS/JS additions

---

## Status

**Status**: 📋 Planning
**Priority**: High
**Estimated Effort**: Medium-High

