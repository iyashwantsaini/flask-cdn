**STEPS**

## 1. Create the directory for adding packages for NPM

```
mkdir npm
mkdir npm/dist
cd npm
```

## 2. Create a package.json file for your package

```
npm init
```

```
{
  "name": "depbot",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "repository": {
    "type": "git",
    "url": "git+https://github.com/meyash/dep_bot.git"
  },
  "author": "Yashwant",
  "license": "ISC",
  "bugs": {
    "url": "https://github.com/meyash/dep_bot/issues"
  },
  "homepage": "https://github.com/meyash/dep_bot#readme"
}
```

## 3. Create a index.js

```
vim dist/index.js
```

## 4. Copy all your static content to dist directory

Now lets copy all our static content to the dist directory. All CSS,JS,Images are here.

## 5. Publish you static content as package in NPM

Now we are all set, let’s connect to NPM and publish our package.

```
npm login
Username: meyash
Password: i#tYD5*VzD;_riS
Email: (this IS public) yashsn2127@gmail.com
Logged in as meyash on https://registry.npmjs.org/.
```
```
npm publish
```

## 6. Verify published package in NPM

Lets try to access it using unpkg. Open your browser and enter the url in the below format.<br>
https://unpkg.com/pacakage/<br>
For using specific version https://unpkg.com/package@version/:file<br>

Example :
```
<script src="https://unpkg.com/depbot@1.0.0/dist/index.js"></script>
<link href="https://unpkg.com/depbot@1.0.0/dist/index.css" rel="stylesheet" type="text/css">
```