import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowLeft, Phone, MapPin, AlertCircle, Map } from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const serviceIcons = {
  "Emergency": "🚨",
  "Police": "👮",
  "Hospital": "🏥",
  "Ambulance": "🚑",
  "Fire Station": "🚒",
  "Women Helpline": "👩",
  "Child Helpline": "👶",
  "Tourist Helpline": "🗺️",
  "Municipal Office": "🏛️",
  "Electricity Emergency": "⚡",
  "Water Supply": "💧",
  "Disaster Management": "🌪️"
};

const CityPage = () => {
  const { citySlug } = useParams();
  const navigate = useNavigate();
  const [cityData, setCityData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchCityServices();
  }, [citySlug]);

  const fetchCityServices = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get(`${API}/cities/${citySlug}`);
      setCityData(response.data);
    } catch (error) {
      console.error("Error fetching city services:", error);
      if (error.response && error.response.status === 404) {
        navigate("/error");
      } else {
        setError("Failed to load services. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading services...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white flex items-center justify-center">
        <div className="text-center">
          <AlertCircle className="h-16 w-16 text-red-500 mx-auto mb-4" />
          <p className="text-gray-800 text-lg mb-4">{error}</p>
          <Button onClick={() => navigate("/")} className="bg-blue-600 hover:bg-blue-700">
            Go Back Home
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-blue-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <Button
            onClick={() => navigate("/")}
            variant="ghost"
            className="mb-4 text-blue-600 hover:text-blue-700 hover:bg-blue-50"
            data-testid="back-button"
          >
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Home
          </Button>
          <div className="flex items-center space-x-3">
            <MapPin className="h-8 w-8 text-blue-600" />
            <div>
              <h1 className="text-3xl font-semibold text-blue-900" data-testid="city-name">
                {cityData?.name}
              </h1>
              <div className="flex items-center text-blue-700 mt-1">
                <Map className="h-4 w-4 mr-1" />
                <p className="text-sm" data-testid="state-name">{cityData?.state_name}</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Services Grid */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="mb-8">
          <h2 className="text-2xl font-semibold text-gray-900 mb-2">Essential Services ({cityData?.services?.length || 0})</h2>
          <p className="text-gray-600">Emergency and essential services available in {cityData?.name}</p>
        </div>

        {cityData?.services && cityData.services.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" data-testid="services-grid">
            {cityData.services.map((service, index) => (
              <Card key={index} className="border-blue-100 shadow-sm hover:shadow-md transition-shadow" data-testid={`service-card-${service.service_type.toLowerCase().replace(/\s+/g, '-')}`}>
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex items-center space-x-3">
                      <span className="text-4xl">{serviceIcons[service.service_type] || "📋"}</span>
                      <div>
                        <CardTitle className="text-lg text-gray-900" data-testid={`service-type-${service.service_type.toLowerCase().replace(/\s+/g, '-')}`}>
                          {service.service_type}
                        </CardTitle>
                      </div>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-gray-600 text-sm mb-4" data-testid={`service-description-${service.service_type.toLowerCase().replace(/\s+/g, '-')}`}>
                    {service.description}
                  </CardDescription>
                  <div className="flex items-center space-x-2 bg-blue-50 p-3 rounded-lg">
                    <Phone className="h-5 w-5 text-blue-600 flex-shrink-0" />
                    <a
                      href={`tel:${service.contact}`}
                      className="text-blue-700 font-semibold text-base hover:text-blue-800 break-all"
                      data-testid={`service-contact-${service.service_type.toLowerCase().replace(/\s+/g, '-')}`}
                    >
                      {service.contact}
                    </a>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        ) : (
          <div className="text-center py-12 bg-white rounded-lg border border-blue-100">
            <p className="text-gray-600">No services available for this city.</p>
          </div>
        )}

        {/* Important Notice */}
        <div className="mt-12 bg-blue-50 border border-blue-200 rounded-lg p-6">
          <div className="flex items-start space-x-3">
            <AlertCircle className="h-6 w-6 text-blue-600 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold text-blue-900 mb-1">Important Information</h3>
              <p className="text-blue-800 text-sm">
                For life-threatening emergencies, always dial <strong>112</strong> (National Emergency Number) immediately.
                The information provided here is for reference purposes. Some contact numbers may vary by city.
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default CityPage;