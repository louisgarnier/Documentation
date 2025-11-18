# Phase 3: React Frontend Development

## Status: ⏭️ Future Phase

This phase will create a modern React frontend (Next.js or Nuxt.js) matching the design from `test-case-manager/`.

## Objectives

1. Choose frontend framework (Next.js recommended)
2. Initialize project
3. Copy and adapt components from test-case-manager
4. Create API client
5. Implement all features
6. Test frontend

## Framework Choice

### Next.js (Recommended)
- **Pros**: React-based, SSR, great DX, TypeScript support
- **Cons**: None significant

### Nuxt.js
- **Pros**: Vue-based, similar to Next.js
- **Cons**: Different ecosystem than test-case-manager (React)

**Decision**: Next.js (matches test-case-manager React components)

## Components to Implement

Based on `test-case-manager/` components:

1. **Header.tsx** - Sticky header with title/subtitle
2. **TestCaseList.tsx** - Container for test case cards
3. **TestCaseItem.tsx** - Individual test case card
4. **TestCaseDetail.tsx** - Detail view with back button
5. **Footer.tsx** - Conditional footer with export
6. **Icons** - CheckIcon, ChevronLeftIcon

## Features to Implement

- ✅ Test case list with card-based layout
- ✅ Test case detail view
- ✅ Create new test case
- ✅ Edit test case
- ✅ Delete test case
- ✅ Add/edit/delete steps
- ✅ Screenshot upload/display/delete
- ✅ Step reordering
- ✅ Excel export
- ✅ Selection checkboxes
- ✅ Status badges (if implemented)

## API Client

Create API client to communicate with backend:

```typescript
// frontend/src/api/client.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = {
  getTestCases: () => fetch(`${API_BASE_URL}/api/test-cases`),
  getTestCase: (id: number) => fetch(`${API_BASE_URL}/api/test-cases/${id}`),
  // ... etc
};
```

## Implementation Steps

1. **Initialize Next.js project**
   ```bash
   cd frontend
   npx create-next-app@latest . --typescript --tailwind --app
   ```

2. **Install dependencies**
   ```bash
   npm install axios  # or fetch API
   npm install lucide-react  # for icons (matching test-case-manager)
   ```

3. **Copy components from test-case-manager**
   - Adapt TypeScript types
   - Update API calls
   - Match styling

4. **Create API client**
   - `frontend/src/api/client.ts`
   - Handle requests/responses
   - Error handling

5. **Implement pages**
   - List page
   - Detail page
   - Create/edit forms

6. **Styling**
   - Use Tailwind CSS (matching test-case-manager)
   - Dark theme support
   - Responsive design

7. **Testing**
   - Test all features
   - Test API integration
   - Test responsive design

## File Structure

```
frontend/
├── src/
│   ├── app/              # Next.js app directory
│   │   ├── page.tsx      # List page
│   │   ├── test-case/
│   │   │   └── [id]/
│   │   │       └── page.tsx  # Detail page
│   ├── components/
│   │   ├── Header.tsx
│   │   ├── TestCaseList.tsx
│   │   ├── TestCaseItem.tsx
│   │   ├── TestCaseDetail.tsx
│   │   ├── Footer.tsx
│   │   └── icons/
│   ├── api/
│   │   └── client.ts
│   └── types/
│       └── index.ts
├── package.json
└── README.md
```

## Dependencies

```json
{
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "axios": "^1.6.0",
    "lucide-react": "^0.294.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^18.0.0",
    "typescript": "^5.0.0",
    "tailwindcss": "^3.3.0"
  }
}
```

## Design Reference

Match the design from `../test-case-manager/`:
- Color scheme (HSL values)
- Card layout
- Typography
- Spacing
- Hover effects
- Status badges

## Next Steps

After Phase 3 completion:
- ✅ Phase 3: React Frontend Development
- ⏭️ Phase 4: Integration & Testing

