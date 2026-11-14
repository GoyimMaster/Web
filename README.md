# aistudious.ca

Static site (GitHub Pages). No build step is needed to publish; `python3 build.py` only regenerates the pages and art from the templates in `build.py`.

## Things you change in `config.js` (no rebuild)
- **Videos:** put the file in `videos/`, then set `src` for a slot (`reel`, `w1` … `w9`). Optional: `poster` (image shown before play), `title`, `tag`. Empty slots show "Coming soon". Keep files small (under ~25 MB each); for longer videos host them elsewhere and paste the URL as `src`.
- **Calendly:** paste your event link into `calendly`. "Book a call" buttons then open the Calendly popup and the Contact page shows the calendar.
- **Inquiry form:** paste a form endpoint into `formEndpoint` (Formspree or Web3Forms; for Web3Forms also set `formAccessKey`). Until then the form opens the visitor's email app with the message filled in.

## Publish
`git add -A && git commit -m "Update site" && git push`
