import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { MapPin, Building2, Map } from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const HomePage = () => {
  const [states, setStates] = useState([]);
  const [cities, setCities] = useState([]);
  const [selectedState, setSelectedState] = useState("");
  const [selectedCity, setSelectedCity] = useState("");
  const [loadingStates, setLoadingStates] = useState(true);
  const [loadingCities, setLoadingCities] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    fetchStates();
  }, []);

  useEffect(() => {
    if (selectedState) {
      fetchCities(selectedState);
      setSelectedCity(""); // Reset city selection when state changes
    } else {
      setCities([]);
    }
  }, [selectedState]);

  const fetchStates = async () => {
    try {
      setLoadingStates(true);
      const response = await axios.get(`${API}/states`);
      setStates(response.data);
    } catch (error) {
      console.error("Error fetching states:", error);
    } finally {
      setLoadingStates(false);
    }
  };

  const fetchCities = async (stateSlug) => {
    try {
      setLoadingCities(true);
      const response = await axios.get(`${API}/cities?state=${stateSlug}`);
      setCities(response.data);
    } catch (error) {
      console.error("Error fetching cities:", error);
    } finally {
      setLoadingCities(false);
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
            <div>
              <h1 className="text-3xl font-semibold text-blue-900">AskMyCity</h1>
              <p className="text-sm text-blue-600">India-wide City Services Directory</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="bg-white rounded-xl shadow-lg border border-blue-100 p-8 md:p-12">
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 rounded-full mb-4">
              <MapPin className="h-8 w-8 text-blue-600" />
            </div>
            <h2 className="text-2xl font-semibold text-gray-900 mb-2">Find City Services</h2>
            <p className="text-gray-600">Select your state and city to view emergency and essential services</p>
          </div>

          {loadingStates ? (
            <div className="flex justify-center py-8">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>
          ) : (
            <div className="space-y-6">
              {/* State Selection */}
              <div>
                <label htmlFor="state-select" className="block text-sm font-medium text-gray-700 mb-2">
                  <Map className="inline h-4 w-4 mr-1" />
                  State / Union Territory
                </label>
                <Select onValueChange={setSelectedState} value={selectedState} data-testid="state-select">
                  <SelectTrigger className="w-full h-12 text-base" data-testid="state-select-trigger">
                    <SelectValue placeholder="Choose your state" />
                  </SelectTrigger>
                  <SelectContent data-testid="state-select-content" className="max-h-[300px]">
                    {states.map((state) => (
                      <SelectItem key={state.slug} value={state.slug} data-testid={`state-option-${state.slug}`}>
                        {state.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* City Selection */}
              <div>
                <label htmlFor="city-select" className="block text-sm font-medium text-gray-700 mb-2">
                  <MapPin className="inline h-4 w-4 mr-1" />
                  City
                </label>
                <Select 
                  onValueChange={setSelectedCity} 
                  value={selectedCity}
                  disabled={!selectedState || loadingCities}
                  data-testid="city-select"
                >
                  <SelectTrigger 
                    className="w-full h-12 text-base" 
                    data-testid="city-select-trigger"
                    disabled={!selectedState || loadingCities}
                  >
                    <SelectValue 
                      placeholder={
                        loadingCities 
                          ? "Loading cities..." 
                          : !selectedState 
                          ? "First select a state" 
                          : "Choose your city"
                      } 
                    />
                  </SelectTrigger>
                  <SelectContent data-testid="city-select-content" className="max-h-[300px]">
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

        {/* Info Section */}
        <div className="mt-12">
          <div className="text-center mb-6">
            <h3 className="text-xl font-semibold text-gray-900 mb-2">12 Essential Services Available</h3>
            <p className="text-gray-600">Quick access to all emergency and civic services across India</p>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-white p-4 rounded-lg border border-blue-100 shadow-sm text-center">
              <div className="text-2xl mb-1">🚨</div>
              <p className="text-xs font-medium text-gray-700">Emergency</p>
            </div>
            <div className="bg-white p-4 rounded-lg border border-blue-100 shadow-sm text-center">
              <div className="text-2xl mb-1">👮</div>
              <p className="text-xs font-medium text-gray-700">Police</p>
            </div>
            <div className="bg-white p-4 rounded-lg border border-blue-100 shadow-sm text-center">
              <div className="text-2xl mb-1">🏥</div>
              <p className="text-xs font-medium text-gray-700">Hospital</p>
            </div>
            <div className="bg-white p-4 rounded-lg border border-blue-100 shadow-sm text-center">
              <div className="text-2xl mb-1">🚑</div>
              <p className="text-xs font-medium text-gray-700">Ambulance</p>
            </div>
            <div className="bg-white p-4 rounded-lg border border-blue-100 shadow-sm text-center">
              <div className="text-2xl mb-1">🚒</div>
              <p className="text-xs font-medium text-gray-700">Fire Station</p>
            </div>
            <div className="bg-white p-4 rounded-lg border border-blue-100 shadow-sm text-center">
              <div className="text-2xl mb-1">👩</div>
              <p className="text-xs font-medium text-gray-700">Women Helpline</p>
            </div>
            <div className="bg-white p-4 rounded-lg border border-blue-100 shadow-sm text-center">
              <div className="text-2xl mb-1">👶</div>
              <p className="text-xs font-medium text-gray-700">Child Helpline</p>
            </div>
            <div className="bg-white p-4 rounded-lg border border-blue-100 shadow-sm text-center">
              <div className="text-2xl mb-1">🗺️</div>
              <p className="text-xs font-medium text-gray-700">Tourist Helpline</p>
            </div>
            <div className="bg-white p-4 rounded-lg border border-blue-100 shadow-sm text-center">
              <div className="text-2xl mb-1">🏛️</div>
              <p className="text-xs font-medium text-gray-700">Municipal Office</p>
            </div>
            <div className="bg-white p-4 rounded-lg border border-blue-100 shadow-sm text-center">
              <div className="text-2xl mb-1">⚡</div>
              <p className="text-xs font-medium text-gray-700">Electricity</p>
            </div>
            <div className="bg-white p-4 rounded-lg border border-blue-100 shadow-sm text-center">
              <div className="text-2xl mb-1">💧</div>
              <p className="text-xs font-medium text-gray-700">Water Supply</p>
            </div>
            <div className="bg-white p-4 rounded-lg border border-blue-100 shadow-sm text-center">
              <div className="text-2xl mb-1">🌪️</div>
              <p className="text-xs font-medium text-gray-700">Disaster Mgmt</p>
            </div>
          </div>
        </div>

        {/* Coverage Info */}
        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6 text-center">
          <p className="text-blue-900 font-medium">
            🇮🇳 Covering all 28 States and 8 Union Territories of India
          </p>
          <p className="text-blue-700 text-sm mt-1">
            {states.length} states • Multiple cities per state • 12 services per city
          </p>
        </div>
      </main>
    </div>
  );
};

export default HomePage;