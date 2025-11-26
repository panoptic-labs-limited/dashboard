/**
 * React hooks for dashboard data fetching and rendering.
 */

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../api/client';
import type { DashboardResponse, DashboardRenderResponse } from '../types/dashboard';

/**
 * Fetch dashboard structure by name.
 */
export function useDashboard(name: string) {
  return useQuery({
    queryKey: ['dashboard', name],
    queryFn: () => apiClient.getDashboard(name),
    enabled: !!name,
  });
}

/**
 * Render dashboard with input values.
 */
export function useRenderDashboard(name: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (inputValues: Record<string, any>) =>
      apiClient.renderDashboard(name, inputValues),
    onSuccess: (data) => {
      // Cache the render result
      queryClient.setQueryData(['dashboard-render', name, data.input_values], data);
    },
  });
}

/**
 * Get cached dashboard render result or fetch if not available.
 */
export function useDashboardRender(name: string, inputValues: Record<string, any>) {
  return useQuery({
    queryKey: ['dashboard-render', name, inputValues],
    queryFn: () => apiClient.renderDashboard(name, inputValues),
    enabled: !!name && Object.keys(inputValues).length > 0,
    staleTime: 0, // Always consider stale to allow manual refresh
  });
}

/**
 * Render an individual widget with input values.
 */
export function useWidgetRender(
  dashboardName: string,
  widgetId: string,
  inputValues: Record<string, any>,
  enabled: boolean = true
) {
  return useQuery({
    queryKey: ['widget-render', dashboardName, widgetId, inputValues],
    queryFn: () => apiClient.renderWidget(dashboardName, widgetId, inputValues),
    enabled: enabled && !!dashboardName && !!widgetId,
    staleTime: 0,
  });
}

/**
 * List all available dashboards.
 */
export function useDashboardList() {
  return useQuery({
    queryKey: ['dashboards'],
    queryFn: () => apiClient.listDashboards(),
  });
}
