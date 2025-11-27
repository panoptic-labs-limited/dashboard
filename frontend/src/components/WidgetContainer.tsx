/**
 * Container for individual widget rendering.
 * Handles fetching and rendering a single widget with selector values.
 */

import React from 'react';
import { Card, Elevation, Spinner } from '@blueprintjs/core';
import { useWidgetRender } from '../hooks/useDashboard';
import { Widget } from './Widget';
import type { WidgetSchema } from '../types/dashboard';

interface WidgetContainerProps {
  dashboardName: string;
  widget: WidgetSchema;
  inputValues: Record<string, any>;
}

export const WidgetContainer: React.FC<WidgetContainerProps> = ({
  dashboardName,
  widget,
  inputValues,
}) => {
  // Extract only the input values this widget depends on
  const widgetInputValues = React.useMemo(() => {
    if (!widget.params) return {};

    const relevantInputs: Record<string, any> = {};
    Object.entries(widget.params).forEach(([paramName, paramValue]) => {
      // Check if param is bound to an input
      if (typeof paramValue === 'object' && paramValue?.type === 'input') {
        const inputId = paramValue.input_id;
        if (inputId && inputValues[inputId] !== undefined) {
          relevantInputs[inputId] = inputValues[inputId];
        }
      }
    });
    return relevantInputs;
  }, [widget.params, inputValues]);

  const { data: renderResult, isLoading, error } = useWidgetRender(
    dashboardName,
    widget.id,
    widgetInputValues
  );

  if (isLoading || !renderResult) {
    return (
      <Card elevation={Elevation.TWO}>
        <div style={{ padding: '40px', textAlign: 'center' }}>
          <Spinner size={40} />
          <div style={{ marginTop: '10px', color: '#888' }}>
            Loading {widget.component_alias}...
          </div>
        </div>
      </Card>
    );
  }

  if (error) {
    return (
      <Card elevation={Elevation.TWO}>
        <div style={{ padding: '20px', color: '#c23030' }}>
          Error loading widget: {(error as Error).message}
        </div>
      </Card>
    );
  }

  // Transform the individual widget render result to match the full render format
  const widgetRenderResult = {
    widget_id: renderResult.widget_id,
    component_alias: renderResult.component_alias,
    status: 'success' as const,
    output: renderResult.output,
    execution_time_ms: renderResult.execution_time_ms,
  };

  return <Widget widget={widgetRenderResult} title={widget.title} />;
};
