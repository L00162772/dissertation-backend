module.exports = {
    clearMocks: false,
    collectCoverage: true,
    collectCoverageFrom: ["./*.js"],
    coverageDirectory: "coverage",
    coverageProvider: "v8",
  
    testEnvironment: "node",
    testMatch: [
      "**/tests/*test.ts"
    ],
  };