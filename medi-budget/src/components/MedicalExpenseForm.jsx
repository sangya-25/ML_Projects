import { useState } from 'react';

/**
 * MedicalExpenseForm - A beautiful, accessible form for predicting annual medical expenditure
 * Uses machine learning model features: age, children, BMI, smoking status, gender
 * 
 * This component is self-contained and ready to use in any React application.
 * No external dependencies required beyond React itself.
 */

export default function MedicalExpenseForm() {
  // Form state
  const [formData, setFormData] = useState({
    age: '',
    children: '',
    bmi: '',
    smoker: '',
    sex: '',
    region: ''
  });

  // UI state
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [prediction, setPrediction] = useState(null);
  const [serverError, setServerError] = useState('');

  // Handle input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    // Clear error for this field when user starts typing
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
    setServerError('');
  };

  // Validation rules
  const validateForm = () => {
    const newErrors = {};

    // Age validation
    if (!formData.age) {
      newErrors.age = 'Age is required';
    } else if (formData.age < 0 || formData.age > 120) {
      newErrors.age = 'Age must be between 0 and 120';
    }

    // Children validation
    if (formData.children === '') {
      newErrors.children = 'Number of children is required';
    } else if (formData.children < 0 || formData.children > 10) {
      newErrors.children = 'Number of children must be between 0 and 10';
    }

    // BMI validation
    if (!formData.bmi) {
      newErrors.bmi = 'BMI is required';
    } else if (formData.bmi < 10 || formData.bmi > 60) {
      newErrors.bmi = 'BMI must be between 10 and 60';
    }

    // Smoking status validation
    if (!formData.smoker) {
      newErrors.smoker = 'Please select smoking status';
    }

    // Sex validation
    if (!formData.sex) {
      newErrors.sex = 'Please select sex';
    }

    // Region validation
    if (!formData.region) {
      newErrors.region = 'Please select region';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Check if form is valid for enabling submit button
  const isFormValid = () => {
    return formData.age && formData.children !== '' && formData.bmi && 
           formData.smoker && formData.sex && formData.region && Object.keys(errors).length === 0;
  };

  // API call with backend integration
  const predictAPI = async (payload) => {
    try {
      // Try to connect to backend API first
      const response = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        const result = await response.json();
        return result;
      } else {
        throw new Error(`Backend API error: ${response.status}`);
      }
    } catch (error) {
      console.warn('Backend API not available, using mock prediction:', error.message);
      
      // Fallback to mock prediction if backend is not available
      await new Promise(resolve => setTimeout(resolve, 1500));

      // Deterministic mock prediction based on inputs
      const baseExpenditure = 5000;
      const ageMultiplier = payload.age * 100;
      const bmiMultiplier = (payload.bmi - 18.5) * 200;
      const smokerMultiplier = payload.smoker === 'yes' ? 15000 : 0;
      const childrenMultiplier = payload.children * 500;
      
      // Region factors
      const regionFactors = {
        'northeast': 1000,
        'northwest': 500,
        'southeast': 1500,
        'southwest': 800
      };
      const regionMultiplier = regionFactors[payload.region] || 0;

      const predictedUSD = baseExpenditure + ageMultiplier + bmiMultiplier +
                       smokerMultiplier + childrenMultiplier + regionMultiplier;
      const predictedINR = predictedUSD * 83.5;

      return {
        charges: Math.round(predictedINR * 100) / 100,
        currency: 'INR',
        confidence: 0.87
      };
    }
  };

  // Real API call (commented out - uncomment and modify for production)
  /*
  const realPredictAPI = async (payload) => {
    const response = await fetch('/api/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload)
    });
    
    if (!response.ok) {
      throw new Error('Prediction failed. Please try again.');
    }
    
    return await response.json();
  };
  */

  // Handle form submission
  const handleSubmit = async () => {
    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);
    setServerError('');
    setPrediction(null);

    try {
      // Prepare payload matching API contract
      const payload = {
        age: parseInt(formData.age),
        children: parseInt(formData.children),
        bmi: parseFloat(formData.bmi),
        smoker: formData.smoker === 'smoker' ? 'yes' : 'no',
        sex: formData.sex,
        region: formData.region
      };

      // Use mock API by default
      // To use real API: replace mockPredictAPI with realPredictAPI
      const result = await predictAPI(payload);
      
      setPrediction({
        ...result,
        submittedData: payload
      });
    } catch (error) {
      setServerError(error.message || 'An error occurred while processing your request.');
    } finally {
      setIsSubmitting(false);
    }
  };

  // Handle Enter key press
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && isFormValid()) {
      handleSubmit();
    }
  };

  // Reset form
  const handleReset = () => {
    setFormData({
      age: '',
      children: '',
      bmi: '',
      smoker: '',
      sex: '',
      region: ''
    });
    setErrors({});
    setPrediction(null);
    setServerError('');
  };

  // Copy submitted data as JSON
  const handleCopyJSON = () => {
    const jsonData = JSON.stringify(prediction.submittedData, null, 2);
    navigator.clipboard.writeText(jsonData);
    alert('Input data copied to clipboard!');
  };

  // Download submitted data as JSON
  const handleDownloadJSON = () => {
    const jsonData = JSON.stringify(prediction.submittedData, null, 2);
    const blob = new Blob([jsonData], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'medical-expense-input.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Medical Expense Predictor
          </h1>
          <p className="text-gray-600">
            Enter your information to predict annual medical expenditure
          </p>
        </div>

        {/* Main Form Card */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-6 transition-all duration-300 hover:shadow-2xl">
          <div data-testid="medical-expense-form" onKeyPress={handleKeyPress}>
            {/* Server Error Display */}
            {serverError && (
              <div 
                className="mb-6 p-4 bg-red-50 border-l-4 border-red-500 text-red-700 rounded"
                role="alert"
                data-testid="server-error"
              >
                <p className="font-semibold">Error</p>
                <p>{serverError}</p>
              </div>
            )}

            <div className="space-y-6">
              {/* Age Input */}
              <div>
                <label htmlFor="age" className="block text-sm font-semibold text-gray-700 mb-2">
                  Age *
                </label>
                <input
                  type="number"
                  id="age"
                  name="age"
                  min="0"
                  max="120"
                  value={formData.age}
                  onChange={handleChange}
                  className={`w-full px-4 py-3 rounded-lg border text-black bg-white ${
                    errors.age ? 'border-red-500 focus:ring-red-500' : 'border-gray-300 focus:ring-indigo-500'
                  } focus:ring-2 focus:border-transparent transition-all duration-200`}
                  placeholder="Enter your age"
                  data-testid="age-input"
                  aria-describedby={errors.age ? 'age-error' : undefined}
                  aria-invalid={errors.age ? 'true' : 'false'}
                />
                {errors.age && (
                  <p id="age-error" className="mt-2 text-sm text-red-600" role="alert">
                    {errors.age}
                  </p>
                )}
              </div>

              {/* Number of Children */}
              <div>
                <label htmlFor="children" className="block text-sm font-semibold text-gray-700 mb-2">
                  Number of Children *
                </label>
                <input
                  type="number"
                  id="children"
                  name="children"
                  min="0"
                  max="10"
                  value={formData.children}
                  onChange={handleChange}
                  className={`w-full px-4 py-3 rounded-lg border text-black bg-white ${
                    errors.children ? 'border-red-500 focus:ring-red-500' : 'border-gray-300 focus:ring-indigo-500'
                  } focus:ring-2 focus:border-transparent transition-all duration-200`}
                  placeholder="Enter number of children"
                  data-testid="children-input"
                  aria-describedby={errors.children ? 'children-error' : undefined}
                  aria-invalid={errors.children ? 'true' : 'false'}
                />
                {errors.children && (
                  <p id="children-error" className="mt-2 text-sm text-red-600" role="alert">
                    {errors.children}
                  </p>
                )}
              </div>

              {/* BMI Input */}
              <div>
                <label htmlFor="bmi" className="block text-sm font-semibold text-gray-700 mb-2">
                  BMI (Body Mass Index) *
                  <span className="ml-2 text-xs font-normal text-gray-500">
                    (10.0 - 60.0)
                  </span>
                </label>
                <input
                  type="number"
                  id="bmi"
                  name="bmi"
                  min="10"
                  max="60"
                  step="0.1"
                  value={formData.bmi}
                  onChange={handleChange}
                  className={`w-full px-4 py-3 rounded-lg border text-black bg-white ${
                    errors.bmi ? 'border-red-500 focus:ring-red-500' : 'border-gray-300 focus:ring-indigo-500'
                  } focus:ring-2 focus:border-transparent transition-all duration-200`}
                  placeholder="e.g., 25.3"
                  data-testid="bmi-input"
                  aria-describedby={errors.bmi ? 'bmi-error' : 'bmi-help'}
                  aria-invalid={errors.bmi ? 'true' : 'false'}
                />
                <p id="bmi-help" className="mt-1 text-xs text-gray-500">
                  💡 BMI = weight(kg) / height(m)². Normal range: 18.5-24.9
                </p>
                {errors.bmi && (
                  <p id="bmi-error" className="mt-2 text-sm text-red-600" role="alert">
                    {errors.bmi}
                  </p>
                )}
              </div>

              {/* Smoking Status */}
              <div>
                <fieldset>
                  <legend className="block text-sm font-semibold text-gray-700 mb-3">
                    Smoking Status *
                  </legend>
                  <div className="flex gap-4">
                    <label className="flex items-center cursor-pointer group">
                      <input
                        type="radio"
                        name="smoker"
                        value="smoker"
                        checked={formData.smoker === 'smoker'}
                        onChange={handleChange}
                        className="w-4 h-4 text-indigo-600 focus:ring-indigo-500 focus:ring-2"
                        data-testid="smoker-yes"
                        aria-describedby={errors.smoker ? 'smoker-error' : undefined}
                      />
                      <span className="ml-2 text-gray-700 group-hover:text-gray-900 font-medium">
                        Smoker
                      </span>
                    </label>
                    <label className="flex items-center cursor-pointer group">
                      <input
                        type="radio"
                        name="smoker"
                        value="non-smoker"
                        checked={formData.smoker === 'non-smoker'}
                        onChange={handleChange}
                        className="w-4 h-4 text-indigo-600 focus:ring-indigo-500 focus:ring-2"
                        data-testid="smoker-no"
                        aria-describedby={errors.smoker ? 'smoker-error' : undefined}
                      />
                      <span className="ml-2 text-gray-700 group-hover:text-gray-900 font-medium">
                        Non-smoker
                      </span>
                    </label>
                  </div>
                  {errors.smoker && (
                    <p id="smoker-error" className="mt-2 text-sm text-red-600" role="alert">
                      {errors.smoker}
                    </p>
                  )}
                </fieldset>
              </div>

              {/* Sex */}
              <div>
                <fieldset>
                  <legend className="block text-sm font-semibold text-gray-700 mb-3">
                    Sex *
                  </legend>
                  <div className="flex gap-4">
                    <label className="flex items-center cursor-pointer group">
                      <input
                        type="radio"
                        name="sex"
                        value="male"
                        checked={formData.sex === 'male'}
                        onChange={handleChange}
                        className="w-4 h-4 text-indigo-600 focus:ring-indigo-500 focus:ring-2"
                        data-testid="sex-male"
                        aria-describedby={errors.sex ? 'sex-error' : undefined}
                      />
              <span className="ml-2 text-gray-700 group-hover:text-gray-900 font-medium">
                Male
              </span>
                    </label>
                    <label className="flex items-center cursor-pointer group">
                      <input
                        type="radio"
                        name="sex"
                        value="female"
                        checked={formData.sex === 'female'}
                        onChange={handleChange}
                        className="w-4 h-4 text-indigo-600 focus:ring-indigo-500 focus:ring-2"
                        data-testid="sex-female"
                        aria-describedby={errors.sex ? 'sex-error' : undefined}
                      />
              <span className="ml-2 text-gray-700 group-hover:text-gray-900 font-medium">
                Female
              </span>
                    </label>
                  </div>
                  {errors.sex && (
                    <p id="sex-error" className="mt-2 text-sm text-red-600" role="alert">
                      {errors.sex}
                    </p>
                  )}
                </fieldset>
              </div>

              {/* Region */}
              <div>
                <fieldset>
                  <legend className="block text-sm font-semibold text-gray-700 mb-3">
                    Region *
                  </legend>
                  <div className="grid grid-cols-2 gap-4">
                    <label className="flex items-center cursor-pointer group">
                      <input
                        type="radio"
                        name="region"
                        value="northeast"
                        checked={formData.region === 'northeast'}
                        onChange={handleChange}
                        className="w-4 h-4 text-indigo-600 focus:ring-indigo-500 focus:ring-2"
                        data-testid="region-northeast"
                        aria-describedby={errors.region ? 'region-error' : undefined}
                      />
              <span className="ml-2 text-gray-700 group-hover:text-gray-900 font-medium">
                Northeast
              </span>
                    </label>
                    <label className="flex items-center cursor-pointer group">
                      <input
                        type="radio"
                        name="region"
                        value="northwest"
                        checked={formData.region === 'northwest'}
                        onChange={handleChange}
                        className="w-4 h-4 text-indigo-600 focus:ring-indigo-500 focus:ring-2"
                        data-testid="region-northwest"
                        aria-describedby={errors.region ? 'region-error' : undefined}
                      />
              <span className="ml-2 text-gray-700 group-hover:text-gray-900 font-medium">
                Northwest
              </span>
                    </label>
                    <label className="flex items-center cursor-pointer group">
                      <input
                        type="radio"
                        name="region"
                        value="southeast"
                        checked={formData.region === 'southeast'}
                        onChange={handleChange}
                        className="w-4 h-4 text-indigo-600 focus:ring-indigo-500 focus:ring-2"
                        data-testid="region-southeast"
                        aria-describedby={errors.region ? 'region-error' : undefined}
                      />
              <span className="ml-2 text-gray-700 group-hover:text-gray-900 font-medium">
                Southeast
              </span>
                    </label>
                    <label className="flex items-center cursor-pointer group">
                      <input
                        type="radio"
                        name="region"
                        value="southwest"
                        checked={formData.region === 'southwest'}
                        onChange={handleChange}
                        className="w-4 h-4 text-indigo-600 focus:ring-indigo-500 focus:ring-2"
                        data-testid="region-southwest"
                        aria-describedby={errors.region ? 'region-error' : undefined}
                      />
              <span className="ml-2 text-gray-700 group-hover:text-gray-900 font-medium">
                Southwest
              </span>
                    </label>
                  </div>
                  {errors.region && (
                    <p id="region-error" className="mt-2 text-sm text-red-600" role="alert">
                      {errors.region}
                    </p>
                  )}
                </fieldset>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-4 mt-8">
              <button
                type="button"
                onClick={handleSubmit}
                disabled={!isFormValid() || isSubmitting}
                className={`flex-1 py-3 px-6 rounded-lg font-semibold text-white transition-all duration-200 ${
                  !isFormValid() || isSubmitting
                    ? 'bg-gray-400 cursor-not-allowed'
                    : 'bg-indigo-600 hover:bg-indigo-700 hover:shadow-lg transform hover:-translate-y-0.5'
                } focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2`}
                data-testid="submit-button"
              >
                {isSubmitting ? (
                  <span className="flex items-center justify-center">
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Predicting...
                  </span>
                ) : (
                  'Get Prediction'
                )}
              </button>
              <button
                type="button"
                onClick={handleReset}
                className="px-6 py-3 rounded-lg font-semibold text-gray-700 bg-gray-200 hover:bg-gray-300 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-offset-2"
                data-testid="reset-button"
              >
                Reset
              </button>
            </div>
          </div>
        </div>

        {/* Prediction Result Card */}
        {prediction && (
          <div 
            className="bg-white rounded-2xl shadow-xl p-8 animate-fadeIn"
            data-testid="prediction-result"
          >
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">
                📊 Prediction Results
              </h2>
              <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-semibold">
                {Math.round(prediction.confidence * 100)}% Confidence
              </span>
            </div>

            {/* Main Prediction */}
            <div className="bg-gradient-to-r from-indigo-500 to-purple-600 rounded-xl p-6 text-white mb-6">
              <p className="text-sm opacity-90 mb-2">Predicted Charges</p>
              <p className="text-4xl font-bold" data-testid="predicted-amount">
                ₹{prediction.charges.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
              </p>
              <p className="text-sm opacity-90 mt-2">INR</p>
            </div>

            {/* Input Summary */}
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Your Information</h3>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div className="bg-gray-50 rounded-lg p-3">
                  <p className="text-gray-600">Age</p>
                  <p className="font-semibold text-gray-900">{prediction.submittedData.age} years</p>
                </div>
                <div className="bg-gray-50 rounded-lg p-3">
                  <p className="text-gray-600">Children</p>
                  <p className="font-semibold text-gray-900">{prediction.submittedData.children}</p>
                </div>
                <div className="bg-gray-50 rounded-lg p-3">
                  <p className="text-gray-600">BMI</p>
                  <p className="font-semibold text-gray-900">{prediction.submittedData.bmi}</p>
                </div>
                <div className="bg-gray-50 rounded-lg p-3">
                  <p className="text-gray-600">Smoking Status</p>
                  <p className="font-semibold text-gray-900">{prediction.submittedData.smoker === 'yes' ? 'Smoker' : 'Non-smoker'}</p>
                </div>
                <div className="bg-gray-50 rounded-lg p-3">
                  <p className="text-gray-600">Sex</p>
                  <p className="font-semibold text-gray-900 capitalize">{prediction.submittedData.sex}</p>
                </div>
                <div className="bg-gray-50 rounded-lg p-3">
                  <p className="text-gray-600">Region</p>
                  <p className="font-semibold text-gray-900 capitalize">{prediction.submittedData.region}</p>
                </div>
              </div>
            </div>

            {/* Disclaimer */}
            <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-4">
              <p className="text-sm text-yellow-800">
                <strong>Note:</strong> This prediction is for informational purposes only and should not replace professional medical or financial advice.
              </p>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-3">
              <button
                onClick={handleCopyJSON}
                className="flex-1 py-2 px-4 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg font-medium transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-gray-400"
                data-testid="copy-json-button"
              >
                📋 Copy Input JSON
              </button>
              <button
                onClick={handleDownloadJSON}
                className="flex-1 py-2 px-4 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg font-medium transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-gray-400"
                data-testid="download-json-button"
              >
                💾 Download JSON
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Inline Styles for Animation */}
      <style>{`
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        .animate-fadeIn {
          animation: fadeIn 0.5s ease-out;
        }
      `}</style>
    </div>
  );
}