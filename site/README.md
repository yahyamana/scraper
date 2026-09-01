# Meridian ATM Group — marketing site

A single-page static site: free ATM placement, servicing, and processing
partnerships, with an enquiry form and a live location counter.

Built on the Landwind template (Tailwind CSS + Flowbite), MIT licensed.
The design is unchanged; the content, structure and behaviour are ours.

## Before you launch

Four things are placeholders. Search for `SET ME` and `EDIT ME` in
`index.html` to find them all.

| What | Where | Now |
|---|---|---|
| Enquiry form endpoint | `index.html` — `<form action>` | `https://formspree.io/f/YOUR_FORM_ID` |
| Phone and email | `index.html` — footer "Get in touch" | `(555) 010-4477`, `hello@meridianatmgroup.com` |
| Domain | `index.html` — `<link rel="canonical">` and the `og:`/`twitter:` tags | `www.meridianatmgroup.com` |
| Supporting stats | `index.html` — `#network` section | 99.7% uptime, 48h install, 24/7 monitoring |

The **280+ location count** is real and lives in one place — the
`data-target` attribute on the first `.js-counter`. Update the attribute
*and* the text inside the span, so the correct number shows before
JavaScript runs:

```html
<span class="js-counter" data-target="280" data-suffix="+">280+</span>
```

The four legal links in the footer point at `#contact` until real pages
exist.

## Connecting the form

1. Create a form at [formspree.io](https://formspree.io) and copy its endpoint.
2. Replace `YOUR_FORM_ID` in the `<form action>` in `index.html`.

Submissions go over `fetch`, so the visitor stays on the page and sees an
inline confirmation. If the endpoint fails, the message falls back to
"email us instead" rather than silently dropping the enquiry. Until the
endpoint is set, submitting shows a warning rather than posting nowhere.

Any endpoint that accepts a `POST` of form data works — Formspree is not
special here.

## Developing

```
npm install
npm run dev      # rebuild output.css on change
npm run build    # minified production stylesheet
```

`vendor/flowbite.min.js` is committed so the page has no runtime CDN
dependency. After bumping Flowbite, re-copy it:

```
npm run vendor
```

## Deploying

Upload these and nothing else:

```
index.html  output.css  js/  vendor/  images/  site.webmanifest  *.png  *.ico
```

No build step runs at deploy time. Every path in the page is relative, so
it works from a subdirectory as well as a domain root.

## Notes

- Dark mode uses Tailwind's `class` strategy. The toggle in the header
  writes to `localStorage`; a first-time visitor gets their OS preference,
  applied inline in `<head>` so there is no white flash. If you change
  `darkMode` in `tailwind.config.js`, the toggle stops working.
- Counters animate on scroll and are skipped under
  `prefers-reduced-motion`; the final value is in the HTML either way.
- The template's stock customer-logo strip (Airbnb, Google, Microsoft and
  so on) was removed rather than restyled — those are not our customers.
  The location counter took its slot.
