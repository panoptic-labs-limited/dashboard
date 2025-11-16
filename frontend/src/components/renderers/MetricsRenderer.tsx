/**
 * Metrics/stats card renderer component.
 */

import React from 'react';
import { Card, Elevation } from '@blueprintjs/core';
import type { RenderOutput } from '../../types/dashboard';

interface MetricsRendererProps {
  output: RenderOutput | Record<string, any>;
  title?: string;
}

export const MetricsRenderer: React.FC<MetricsRendererProps> = ({ output, title }) => {
  // Handle both RenderOutput format and direct custom format
  const metricsData = 'type' in output && output.type === 'custom'
    ? output.data
    : output;

  if (!metricsData || !metricsData.data) {
    return (
      <Card elevation={Elevation.TWO}>
        <div style={{ padding: '20px', color: '#888' }}>
          Invalid metrics data
        </div>
      </Card>
    );
  }

  const metrics = metricsData.data;

  return (
    <Card elevation={Elevation.TWO}>
      {title && (
        <div style={{ padding: '15px 20px', borderBottom: '1px solid #e1e8ed' }}>
          <h3 style={{ margin: 0, fontSize: '16px', fontWeight: 600 }}>{title}</h3>
        </div>
      )}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '20px',
        padding: '20px'
      }}>
        {Object.entries(metrics).map(([key, value]) => (
          <div key={key} style={{
            padding: '15px',
            background: '#f5f8fa',
            borderRadius: '6px',
            border: '1px solid #e1e8ed'
          }}>
            <div style={{
              fontSize: '12px',
              color: '#5c7080',
              marginBottom: '8px',
              fontWeight: 500,
              textTransform: 'uppercase',
              letterSpacing: '0.5px'
            }}>
              {key}
            </div>
            <div style={{
              fontSize: '24px',
              fontWeight: 600,
              color: '#182026'
            }}>
              {String(value)}
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
};
