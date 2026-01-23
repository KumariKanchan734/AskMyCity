import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { AlertCircle, Home } from "lucide-react";

const ErrorPage = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white flex items-center justify-center px-4">
      <div className="text-center max-w-md">
        <div className="inline-flex items-center justify-center w-20 h-20 bg-red-100 rounded-full mb-6">
          <AlertCircle className="h-10 w-10 text-red-600" />
        </div>
        
        <h1 className="text-4xl font-bold text-gray-900 mb-4" data-testid="error-title">
          Oops! City Not Found
        </h1>
        
        <p className="text-lg text-gray-600 mb-8" data-testid="error-message">
          The city you're looking for doesn't exist in our database, or the page you're trying to access is unavailable.
        </p>
        
        <Button
          onClick={() => navigate("/")}
          className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 h-12"
          data-testid="home-button"
        >
          <Home className="mr-2 h-5 w-5" />
          Back to Home
        </Button>
      </div>
    </div>
  );
};

export default ErrorPage;