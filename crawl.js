const http = require('http');
const url = require('url');

const BASE_URL = 'http://localhost:5001';

// Directories to crawl
const directories = [
  "/app",
  "/app/static",
  "/app/templates",
  "/node_app"
];

// Directories to ignore
const directoriesToIgnore = [
  "node_modules"
];

// Files to read
const filesToRead = [
  "index.html",
  "debug_node_app_after_npm_install.txt",
  "debug_node_app_build.txt",
  "debug_app_static.txt",
  "debug_app.txt"
];

// Function to make HTTP GET requests
const httpGet = (endpoint) => {
  return new Promise((resolve, reject) => {
    console.log(`Requesting URL: ${endpoint}`);
    const reqUrl = url.parse(endpoint);
    const options = {
      hostname: reqUrl.hostname,
      port: reqUrl.port,
      path: reqUrl.path,
      method: 'GET',
    };

    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => {
        data += chunk;
      });
      res.on('end', () => {
        resolve(data);
      });
    });

    req.on('error', (e) => {
      reject(e.message);
    });

    req.end();
  });
};

// Function to check if a path should be ignored
const shouldIgnore = (path) => path.includes('node_modules');

// Function to list directory contents recursively
const listDir = async (path) => {
    try {
      const endpoint = `${BASE_URL}/list_dir?path=${encodeURIComponent(path)}`;
      const response = await httpGet(endpoint);
      const dirContent = JSON.parse(response);
      console.log(`\nListing contents of directory: ${path}`);
      console.log(response);
  
      for (const dirPath in dirContent) {
        if (dirContent[dirPath] && dirContent[dirPath].dirs) {
          for (const dir of dirContent[dirPath].dirs) {
            const fullPath = `${dirPath}/${dir}`;
            console.log(`Checking if ${fullPath} should be ignored, ${shouldIgnore(fullPath)}`);
            if (shouldIgnore(fullPath)) {
              console.log(`Ignoring directory: ${fullPath}`);
            } else {
              await listDir(fullPath);
            }
          }
        }
  
        if (dirContent[dirPath] && dirContent[dirPath].files) {
          for (const file of dirContent[dirPath].files) {
            const fullPath = `${dirPath}/${file}`;
            if (filesToRead.includes(file) &&!shouldIgnore(fullPath)) {
              await readFile(fullPath);
            }
          }
        }
      }
    } catch (error) {
      console.error(`Error listing directory ${path}:`, error);
    }
  };
  

// Function to read file contents
const readFile = async (path) => {
  try {
    if (shouldIgnore(path)) {
      console.log(`Ignoring file: ${path}`);
      return;
    }

    const endpoint = `${BASE_URL}/read_file?path=${encodeURIComponent(path)}`;
    const response = await httpGet(endpoint);
    console.log(`\nReading contents of file: ${path}`);
    console.log(response);
  } catch (error) {
    console.error(`Error reading file ${path}:`, error);
  }
};

// Crawl directories and files recursively
const crawlDirectories = async () => {
  for (const dir of directories) {
    await listDir(dir);
  }
};

// Run the crawler
crawlDirectories();
