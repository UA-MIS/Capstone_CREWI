For now, let's just make the one-page in here as a React App.

The widget can be a part of it; we can encapsulate it later. In theory, we should be able to compile it with parcel and reference it in the one-page.

If any of that sounds weird or doesn't sound right, you probably know the structure better than I do so feel free to make a judgement call on folder structure.

SET-UP:
git pull
npm install
npm start
*may need to open and save package.json the first time*

NOTES:
If you get a "LF will be replaced..." type warning on git add ., just ignore it for now
If you get a crash the first time you try to open up try opening and saving package.json

index.js is the starting point

public/index.html is where the page will actually load; for the most part you shouldn't alter it directly
