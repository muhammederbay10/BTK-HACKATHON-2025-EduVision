# EduVision - Attention Tracking Platform

An AI-powered platform for analyzing student attention and engagement in educational videos.

## Project Structure

```
project/
├── app/                    # Next.js frontend application
├── backend/               # FastAPI backend server
├── components/            # React UI components
├── lib/                   # Utility functions
└── hooks/                 # Custom React hooks
```

## Prerequisites

- **Node.js** (version 18 or higher)
- **Python** (version 3.8 or higher)
- **npm** or **yarn**

## Installation & Setup

### 1. Frontend Setup (Next.js)

Navigate to the project root directory and install dependencies:

```bash
cd /path/to/project
npm install
```

### 2. Backend Setup (Python/FastAPI)

Navigate to the backend directory and set up a virtual environment:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install Python dependencies:

```bash
pip install --upgrade pip
pip install fastapi uvicorn sqlalchemy python-multipart pydantic
```

## Running the Application

### 1. Start the Backend Server

From the `backend` directory with the virtual environment activated:

```bash
cd backend
source venv/bin/activate
python app/main.py
```

The backend API will be available at: `http://localhost:8000`
- API documentation: `http://localhost:8000/docs`

### 2. Start the Frontend Server

From the project root directory:

```bash
npm run dev
```

The frontend application will be available at: `http://localhost:3000`

## Features

- **Video Upload**: Upload educational videos for analysis
- **Attention Tracking**: AI-powered analysis of student engagement
- **Real-time Processing**: Track analysis progress with live updates
- **Detailed Reports**: Comprehensive insights and recommendations
- **History Management**: View and manage previous analyses

## API Endpoints

- `GET /` - Health check
- `POST /api/upload` - Upload video for analysis
- `GET /api/report/{report_id}` - Get detailed report
- `GET /api/reports` - List all reports
- `GET /api/processing/{report_id}` - Get processing status

## Development

### Frontend Development
```bash
npm run dev     # Start development server
npm run build   # Build for production
npm run start   # Start production server
npm run lint    # Run ESLint
```

### Backend Development
```bash
# With virtual environment activated
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Technology Stack

### Frontend
- **Next.js 13** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Radix UI** - Component library
- **Framer Motion** - Animations

### Backend
- **FastAPI** - Python web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **SQLAlchemy** - Database ORM

## Troubleshooting

### Common Issues

1. **Port conflicts**: If ports 3000 or 8000 are in use, modify the configuration:
   - Frontend: Set `PORT=3001` environment variable
   - Backend: Change port in `app/main.py`

2. **Python virtual environment**: Always activate the virtual environment before running backend commands:
   ```bash
   source backend/venv/bin/activate
   ```

3. **CORS issues**: The backend is configured to allow requests from `http://localhost:3000`. Update CORS settings in `backend/app/main.py` if using different ports.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.
