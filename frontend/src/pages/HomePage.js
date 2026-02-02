import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { Button } from "../components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";
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
      console.log("Cities fetched:", response.data);
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
    <div className="min-h-screen bg-gray-50 font-sans text-gray-900">
      {/* Hero Section */}
      <div className="bg-blue-600 text-white pb-24 pt-10 px-4 relative overflow-hidden">
        <div className="absolute top-0 left-0 w-full h-full opacity-10 pointer-events-none">
          <div className="absolute top-10 left-10 w-20 h-20 rounded-full bg-white blur-xl"></div>
          <div className="absolute bottom-10 right-10 w-32 h-32 rounded-full bg-white blur-2xl"></div>
        </div>

        <div className="max-w-6xl mx-auto relative z-10">
          <div className="flex items-center space-x-3 mb-8">
            <div className="bg-white/20 backdrop-blur-md p-2 rounded-lg">
              <Building2 className="h-8 w-8 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold tracking-tight">AskMyCity</h1>
            </div>
          </div>

          <div className="text-center max-w-2xl mx-auto mt-12 mb-12">
            <h1 className="text-4xl md:text-5xl font-extrabold mb-6 leading-tight">
              India's Essential Service Directory
            </h1>
            <p className="text-blue-100 text-lg md:text-xl leading-relaxed">
              Instantly find and call emergency, civic, and essential services for over 100+ cities across India.
            </p>
          </div>
        </div>
      </div>

      {/* Main Content Card - Floating effect */}
      <main className="max-w-4xl mx-auto px-4 -mt-16 relative z-20 mb-20">
        <div className="bg-white rounded-2xl shadow-xl border border-blue-50 p-6 md:p-10">
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-14 h-14 bg-blue-50 rounded-full mb-4 ring-4 ring-blue-50/50">
              <MapPin className="h-7 w-7 text-blue-600" />
            </div>
            <h2 className="text-2xl font-bold text-gray-900">Find Services Near You</h2>
            <p className="text-gray-500 mt-2">Select your location to get started</p>
          </div>

          {loadingStates ? (
            <div className="flex flex-col items-center justify-center py-12 space-y-4">
              <div className="animate-spin rounded-full h-12 w-12 border-4 border-blue-200 border-t-blue-600"></div>
              <p className="text-blue-600 font-medium">Loading India's data...</p>
            </div>
          ) : (
            <div className="space-y-6 max-w-xl mx-auto">
              {/* State Selection */}
              <div className="space-y-2">
                <label className="text-sm font-semibold text-gray-700 flex items-center">
                  <Map className="w-4 h-4 mr-2 text-blue-500" />
                  State / Union Territory
                </label>
                <Select onValueChange={setSelectedState} value={selectedState}>
                  <SelectTrigger className="w-full h-14 text-base bg-gray-50 border-gray-200 focus:ring-blue-500 rounded-xl transition-all hover:bg-white hover:border-blue-300">
                    <SelectValue placeholder="Select State" />
                  </SelectTrigger>
                  <SelectContent className="max-h-[300px]">
                    {states.map((state) => (
                      <SelectItem key={state.slug} value={state.slug} className="py-3 cursor-pointer">
                        {state.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* City Selection */}
              <div className="space-y-2">
                <label className="text-sm font-semibold text-gray-700 flex items-center">
                  <MapPin className="w-4 h-4 mr-2 text-blue-500" />
                  City
                </label>
                <Select
                  onValueChange={setSelectedCity}
                  value={selectedCity}
                  disabled={!selectedState || loadingCities}
                >
                  <SelectTrigger
                    className="w-full h-14 text-base bg-gray-50 border-gray-200 focus:ring-blue-500 rounded-xl transition-all hover:bg-white hover:border-blue-300 disabled:opacity-50"
                  >
                    <SelectValue
                      placeholder={
                        loadingCities
                          ? "Loading cities..."
                          : !selectedState
                            ? "Select State First"
                            : "Select City"
                      }
                    />
                  </SelectTrigger>
                  <SelectContent className="max-h-[300px]">
                    {Array.isArray(cities) && cities.map((city) => (
                      <SelectItem key={city.slug} value={city.slug} className="py-3 cursor-pointer">
                        {city.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <Button
                onClick={handleSubmit}
                disabled={!selectedCity}
                className="w-full h-14 text-lg font-bold bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white rounded-xl shadow-lg shadow-blue-200 hover:shadow-xl hover:shadow-blue-300 transition-all transform hover:-translate-y-0.5 disabled:shadow-none disabled:bg-gray-300"
              >
                View City Services
              </Button>
            </div>
          )}
        </div>

        {/* Info Grid */}
        <div className="mt-16">
          <div className="text-center mb-8">
            <h3 className="text-xl font-bold text-gray-900">Everything You Need</h3>
            <p className="text-gray-500 mt-2">One platform for all civic and emergency contacts</p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { icon: "🚨", label: "Emergency" },
              { icon: "👮", label: "Police" },
              { icon: "🏥", label: "Hospital" },
              { icon: "🚑", label: "Ambulance" },
              { icon: "🚒", label: "Fire" },
              { icon: "👩", label: "Women Help" },
              { icon: "👶", label: "Child Help" },
              { icon: "⚡", label: "Electricity" },
            ].map((item, idx) => (
              <div key={idx} className="bg-white p-4 rounded-xl border border-gray-100 shadow-sm hover:shadow-md hover:border-blue-100 transition-all flex flex-col items-center justify-center space-y-2 group cursor-default">
                <span className="text-3xl group-hover:scale-110 transition-transform">{item.icon}</span>
                <span className="text-xs font-semibold text-gray-600 group-hover:text-blue-600">{item.label}</span>
              </div>
            ))}
          </div>

          <div className="text-center mt-8">
            <p className="text-sm text-gray-400">...and more services like Water, Municipal, and Tourist helplines.</p>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-50 border-t border-gray-200 py-10 text-center">
        <div className="flex items-center justify-center space-x-2 text-blue-900 font-semibold mb-2">
          <Building2 className="h-5 w-5" />
          <span>AskMyCity</span>
        </div>
        <p className="text-gray-500 text-sm">© 2026 AskMyCity. Making cities accessible.</p>
      </footer>
    </div>
  );
};

export default HomePage;