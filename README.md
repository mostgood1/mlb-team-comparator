# MLB Team Comparator

## Overview
The MLB Team Comparator is a TypeScript application that allows users to compare two baseball teams based on their performance statistics retrieved from the MLB API. The application fetches data for specified teams and determines the winner based on their wins, losses, and win percentage.

## Project Structure
```
mlb-team-comparator
├── src
│   ├── app.ts               # Entry point of the application
│   ├── api
│   │   └── mlbApi.ts       # Functions to interact with the MLB API
│   ├── models
│   │   └── team.ts         # Team model representing a baseball team
│   ├── services
│   │   └── compareTeams.ts  # Service to compare two teams
│   └── types
│       └── index.ts        # Type definitions for the project
├── package.json             # npm configuration file
├── tsconfig.json            # TypeScript configuration file
└── README.md                # Project documentation
```

## Installation
To set up the project, clone the repository and install the dependencies:

```bash
git clone <repository-url>
cd mlb-team-comparator
npm install
```

## Usage
To run the application, use the following command:

```bash
npm start
```

You will be prompted to enter the names of the two teams you wish to compare. The application will fetch the relevant data and display the comparison results.

## API Integration
The application interacts with the MLB API to fetch team data. Ensure you have the necessary API keys and configurations set up in the `mlbApi.ts` file.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License.