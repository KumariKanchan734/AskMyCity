import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { MapPin, Building2 } from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const HomePage = () => {
  const [cities, setCities] = useState([]);
  const [selectedCity, setSelectedCity] = useState("");
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchCities();
  }, []);

  const fetchCities = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API}/cities`);
      setCities(response.data);
    } catch (error) {
      console.error("Error fetching cities:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = () => {
    if (selectedCity) {
      navigate(`/city/${selectedCity}`);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-blue-100">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center space-x-3">
            <div className="bg-blue-600 p-2 rounded-lg">
              <Building2 className="h-8 w-8 text-white" />
            </div>
            <h1 className="text-3xl font-semibold text-blue-900">AskMyCity</h1>
          </div>
          <p className="mt-2 text-blue-700">Find important city services instantly</p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="bg-white rounded-xl shadow-lg border border-blue-100 p-8 md:p-12">
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 rounded-full mb-4">
              <MapPin className="h-8 w-8 text-blue-600" />
            </div>
            <h2 className="text-2xl font-semibold text-gray-900 mb-2">Select Your City</h2>
            <p className="text-gray-600">Choose a city to view emergency and essential services</p>
          </div>

          {loading ? (
            <div className="flex justify-center py-8">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>
          ) : (
            <div className="space-y-6">
              <div>
                <label htmlFor="city-select" className="block text-sm font-medium text-gray-700 mb-2">
                  City
                </label>
                <Select onValueChange={setSelectedCity} data-testid="city-select">
                  <SelectTrigger className="w-full h-12 text-base" data-testid="city-select-trigger">
                    <SelectValue placeholder="Choose your city" />
                  </SelectTrigger>
                  <SelectContent data-testid="city-select-content">
                    {cities.map((city) => (
                      <SelectItem key={city.slug} value={city.slug} data-testid={`city-option-${city.slug}`}>
                        {city.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <Button
                onClick={handleSubmit}
                disabled={!selectedCity}
                className="w-full h-12 bg-blue-600 hover:bg-blue-700 text-white text-base font-medium disabled:bg-gray-300 disabled:cursor-not-allowed"
                data-testid="view-services-button"
              >
                View Services
              </Button>
            </div>
          )}
        </div>

        {/* Info Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
          <div className="bg-white p-6 rounded-lg border border-blue-100 shadow-sm">
            <div className="text-3xl mb-2">🚨</div>
            <h3 className="font-semibold text-gray-900 mb-1">Emergency</h3>
            <p className="text-sm text-gray-600">Quick access to emergency services</p>
          </div>
          <div className="bg-white p-6 rounded-lg border border-blue-100 shadow-sm">
            <div className="text-3xl mb-2">🏥</div>
            <h3 className="font-semibold text-gray-900 mb-1">Healthcare</h3>
            <p className="text-sm text-gray-600">Hospital and ambulance contacts</p>
          </div>
          <div className="bg-white p-6 rounded-lg border border-blue-100 shadow-sm">
            <div className="text-3xl mb-2">👮</div>
            <h3 className="font-semibold text-gray-900 mb-1">Police</h3>
            <p className="text-sm text-gray-600">Police helpline numbers</p>
          </div>
        </div>
      </main>
    </div>
  );
};

export default HomePage;