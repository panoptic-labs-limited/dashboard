/**
 * Widget component - renders widget output based on type.
 */

import React from 'react';
import { Card, Elevation, Spinner, Callout, Intent } from '@blueprintjs/core';
import { PlotlyRenderer } from './renderers/PlotlyRenderer';
import { MetricsRenderer } from './renderers/MetricsRenderer';
import type { WidgetRenderResult } from '../types/dashboard';

interface WidgetProps {
  widget: WidgetRenderResult;
  title?: string;
}

export const Widget: React.FC<WidgetProps> = ({ widget, title }) => {
  // Error state
  if (widget.status === 'error' || widget.status === 'timeout') {
    return (
      <Card elevation={Elevation.TWO}>
        {title && (
          <div style={{ padding: '15px 20px', borderBottom: '1px solid #e1e8ed' }}>
            <h3 style={{ margin: 0, fontSize: '16px', fontWeight: 600 }}>{title}</h3>
          </div>
        )}
        <div style={{ padding: '20px' }}>
          <Callout intent={Intent.DANGER} title={widget.status === 'timeout' ? 'Execution Timeout' : 'Execution Error'}>
            {widget.error_message || 'Unknown error occurred'}
          </Callout>
        </div>
      </Card>
    );
  }

  // No output yet
  if (!widget.output) {
    return (
      <Card elevation={Elevation.TWO}>
        {title && (
          <div style={{ padding: '15px 20px', borderBottom: '1px solid #e1e8ed' }}>
            <h3 style={{ margin: 0, fontSize: '16px', fontWeight: 600 }}>{title}</h3>
          </div>
        )}
        <div style={{ padding: '40px', textAlign: 'center' }}>
          <Spinner size={40} />
        </div>
      </Card>
    );
  }

  // Determine output type and render appropriately
  const output = widget.output;

  // Handle RenderOutput format with explicit type
  if ('type' in output && output.type) {
    switch (output.type) {
      case 'plotly':
        return <PlotlyRenderer output={output} title={title} />;

      case 'custom':
        // Check if it's metrics format
        if (output.data && output.data.type === 'metrics') {
          return <MetricsRenderer output={output} title={title} />;
        }
        // Fall through to generic JSON display
        break;

      case 'vega_lite':
      case 'altair':
        // TODO: Implement Vega/Altair renderer
        return (
          <Card elevation={Elevation.TWO}>
            {title && (
              <div style={{ padding: '15px 20px', borderBottom: '1px solid #e1e8ed' }}>
                <h3 style={{ margin: 0, fontSize: '16px', fontWeight: 600 }}>{title}</h3>
              </div>
            )}
            <div style={{ padding: '20px' }}>
              <Callout intent={Intent.WARNING}>
                {output.type} rendering not yet implemented
              </Callout>
            </div>
          </Card>
        );
    }
  }

  // Generic JSON display for unknown formats
  return (
    <Card elevation={Elevation.TWO}>
      {title && (
        <div style={{ padding: '15px 20px', borderBottom: '1px solid #e1e8ed' }}>
          <h3 style={{ margin: 0, fontSize: '16px', fontWeight: 600 }}>{title}</h3>
        </div>
      )}
      <div style={{ padding: '20px' }}>
        <pre style={{
          background: '#f5f8fa',
          padding: '15px',
          borderRadius: '6px',
          overflow: 'auto',
          fontSize: '12px'
        }}>
          {JSON.stringify(output, null, 2)}
        </pre>
      </div>
    </Card>
  );
};
