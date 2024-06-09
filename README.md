# GitToText-Backend

[![GitHub issues](https://img.shields.io/github/issues/bfuerholz/GitToText-Backend)](https://github.com/bfuerholz/GitToText-Backend/issues)
[![GitHub forks](https://img.shields.io/github/forks/bfuerholz/GitToText-Backend)](https://github.com/bfuerholz/GitToText-Backend/network)
[![GitHub stars](https://img.shields.io/github/stars/bfuerholz/GitToText-Backend)](https://github.com/bfuerholz/GitToText-Backend/stargazers)
[![GitHub license](https://img.shields.io/github/license/bfuerholz/GitToText-Backend)](https://github.com/bfuerholz/GitToText-Backend/blob/main/LICENSE)

GitToText-Backend is a Flask-based backend application for the GitToText project. It handles the processing of GitHub repositories and serves the frontend application.

## Features

- **Fetch Files**: Retrieve all files from a specified GitHub repository.
- **Process Content**: Convert and clean the content for easy readability.
- **API Endpoints**: Provide endpoints for the frontend to interact with.

## How to Use

The backend provides an API endpoint that the frontend interacts with to fetch and process repository data.

## Deployment

The backend is deployed on Vercel. Make sure to set up the necessary environment variables and configure the backend URL correctly in the frontend application.

For detailed deployment steps, refer to the Vercel documentation.

## TODOs

1. **Improve Performance**:
    - Implement caching mechanisms to reduce the load on the GitHub API.
    - Use a task queue like Celery to handle long-running tasks asynchronously.
    - Optimize the database queries and interactions.

2. **Enhance Security**:
    - Implement authentication and authorization for API endpoints.
    - Use rate limiting to prevent abuse of the API.
    - Ensure all sensitive data is encrypted both in transit and at rest.

3. **Improve Error Handling**:
    - Enhance logging to provide more context for errors.
    - Implement retries for transient errors when interacting with the GitHub API.
    - Provide detailed error responses to the frontend.

4. **Scalability**:
    - Use a microservices architecture to separate different concerns.
    - Deploy the application using container orchestration tools like Kubernetes.
    - Implement horizontal scaling to handle increased load.

5. **Add Unit and Integration Tests**:
    - Use testing libraries like pytest to write unit and integration tests.
    - Ensure that all critical paths in the application are covered by tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
