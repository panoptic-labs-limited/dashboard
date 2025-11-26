/**
 * API client for Viz registry backend.
 */

import axios, { type AxiosInstance } from 'axios';
import type { DashboardResponse, DashboardRenderResponse } from '../types/dashboard';

export class VizApiClient {
  private client: AxiosInstance;
  private token: string | null = null;

  constructor(baseURL: string = 'http://localhost:8000') {
    this.client = axios.create({
      baseURL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add token to requests if available
    this.client.interceptors.request.use((config) => {
      if (this.token) {
        config.headers.Authorization = `Bearer ${this.token}`;
      }
      return config;
    });
  }

  /**
   * Authenticate with the registry.
   */
  async login(username: string, password: string): Promise<string> {
    const response = await this.client.post<{ access_token: string; token_type: string }>(
      '/auth/login',
      {
        username,
        password,
      }
    );

    this.token = response.data.access_token;
    return this.token;
  }

  /**
   * Set the authentication token.
   */
  setToken(token: string) {
    this.token = token;
  }

  /**
   * Get a dashboard by name.
   */
  async getDashboard(name: string): Promise<DashboardResponse> {
    const response = await this.client.get<DashboardResponse>(`/dashboards/${name}`);
    return response.data;
  }

  /**
   * List all dashboards for the current user.
   */
  async listDashboards(): Promise<DashboardResponse[]> {
    const response = await this.client.get<DashboardResponse[]>('/dashboards/');
    return response.data;
  }

  /**
   * Render a dashboard with input values.
   */
  async renderDashboard(
    name: string,
    inputValues: Record<string, any>
  ): Promise<DashboardRenderResponse> {
    const request = {
      input_values: inputValues,
    };

    const response = await this.client.post<DashboardRenderResponse>(
      `/dashboards/${name}/render`,
      request
    );

    return response.data;
  }

  /**
   * Render an individual widget with input values.
   */
  async renderWidget(
    dashboardName: string,
    widgetId: string,
    inputValues: Record<string, any>
  ): Promise<{
    widget_id: string;
    component_alias: string;
    output: any;
    execution_time_ms: number;
    memory_used_mb?: number;
  }> {
    const response = await this.client.post(
      `/dashboard/${dashboardName}/component/${widgetId}/render`,
      {
        input_values: inputValues,
      }
    );

    return response.data;
  }
}

// Create a default client instance
export const apiClient = new VizApiClient();
