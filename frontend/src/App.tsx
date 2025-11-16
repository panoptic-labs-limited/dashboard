/**
 * Main App component.
 */

import React, { useState } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Dashboard } from './components/Dashboard';
import { apiClient } from './api/client';
import { Button, Card, Elevation, FormGroup, InputGroup, Intent } from '@blueprintjs/core';

// Import Blueprint CSS
import '@blueprintjs/core/lib/css/blueprint.css';
import '@blueprintjs/datetime2/lib/css/blueprint-datetime2.css';
import '@blueprintjs/select/lib/css/blueprint-select.css';
import '@blueprintjs/icons/lib/css/blueprint-icons.css';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [username, setUsername] = useState('testuser');
  const [password, setPassword] = useState('testpassword123');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      await apiClient.login(username, password);
      setIsAuthenticated(true);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Login failed');
    } finally {
      setIsLoading(false);
    }
  };

  // Login screen
  if (!isAuthenticated) {
    return (
      <div style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: '#f5f8fa'
      }}>
        <Card elevation={Elevation.TWO} style={{ width: '400px', padding: '30px' }}>
          <h1 style={{ margin: '0 0 20px 0', fontSize: '24px' }}>Viz Dashboard</h1>
          <form onSubmit={handleLogin}>
            <FormGroup label="Username" labelFor="username">
              <InputGroup
                id="username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Username"
                large
              />
            </FormGroup>

            <FormGroup label="Password" labelFor="password">
              <InputGroup
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
                large
              />
            </FormGroup>

            {error && (
              <div style={{ marginBottom: '15px', color: '#db3737', fontSize: '14px' }}>
                {error}
              </div>
            )}

            <Button
              type="submit"
              intent={Intent.PRIMARY}
              text="Log In"
              large
              fill
              loading={isLoading}
            />
          </form>
        </Card>
      </div>
    );
  }

  // Main dashboard view
  return (
    <QueryClientProvider client={queryClient}>
      <div style={{ minHeight: '100vh', background: '#f5f8fa' }}>
        <Dashboard dashboardName="sales_dashboard" />
      </div>
    </QueryClientProvider>
  );
}

export default App;
