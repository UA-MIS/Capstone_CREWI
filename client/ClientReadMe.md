For now, let's just make the one-page in here as a React App.

The widget can be a part of it; we can encapsulate it later. In theory, we should be able to compile it with parcel and reference it in the one-page.

If any of that sounds weird or doesn't sound right, you probably know the structure better than I do so feel free to make a judgement call on folder structure.

SET-UP:
git pull
npm install
npm start
*may need to open and save package.json the first time*
npm install react-bootstrap

NOTES:
If you get a "LF will be replaced..." type warning on git add ., just ignore it for now
If you get a crash the first time you try to open up try opening and saving package.json

index.js is the starting point

public/index.html is where the page will actually load; for the most part you shouldn't alter it directly

Packages

Chakra-UI: npm i @chakra-ui/react @emotion/react@^11 @emotion/styled@^11 framer-motion@^6 (https://chakra-ui.com/docs/getting-started)

# SETUP
1. Go to client/crewi-dfa-one-page (case sensitive)
2. Download node.js at https://nodejs.org/en/download/
3. Restart your computer
4. Run ```npm install```
5. Run ```npm start```
6. Allow access if prompted