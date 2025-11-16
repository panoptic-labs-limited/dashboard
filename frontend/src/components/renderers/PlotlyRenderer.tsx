/**
 * Plotly chart renderer component.
 */

import React from 'react';
import Plot from 'react-plotly.js';
import { Card, Elevation } from '@blueprintjs/core';
import type { RenderOutput } from '../../types/dashboard';

interface PlotlyRendererProps {
  output: RenderOutput;
  title?: string;
}

export const PlotlyRenderer: React.FC<PlotlyRendererProps> = ({ output, title }) => {
  if (output.type !== 'plotly' || !output.data) {
    return (
      <Card elevation={Elevation.TWO}>
        <div style={{ padding: '20px', color: '#888' }}>
          Invalid Plotly data
        </div>
      </Card>
    );
  }

  const { data, layout, config } = output.data;

  return (
    <Card elevation={Elevation.TWO} style={{ padding: 0 }}>
      {title && (
        <div style={{ padding: '15px 20px', borderBottom: '1px solid #e1e8ed' }}>
          <h3 style={{ margin: 0, fontSize: '16px', fontWeight: 600 }}>{title}</h3>
        </div>
      )}
      <div style={{ padding: '10px', width: '100%', overflow: 'hidden' }}>
        <Plot
          data={data}
          layout={{
            ...layout,
            autosize: true,
            margin: { l: 50, r: 30, t: 30, b: 50 },
          }}
          config={{
            responsive: true,
            displayModeBar: true,
            displaylogo: false,
            ...config,
          }}
          style={{ width: '100%', height: '400px' }}
          useResizeHandler={true}
        />
      </div>
    </Card>
  );
};
