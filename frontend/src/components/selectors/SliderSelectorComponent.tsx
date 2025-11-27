/**
 * Slider selector component using Blueprint Slider.
 */

import React from 'react';
import { FormGroup, Slider } from '@blueprintjs/core';
import type { SliderSchema } from '../../types/dashboard';

interface SliderSelectorComponentProps {
  selector: SliderSchema;
  value: number | null;
  onChange: (value: number | null) => void;
}

export const SliderSelectorComponent: React.FC<SliderSelectorComponentProps> = ({
  selector,
  value,
  onChange,
}) => {
  const handleChange = (newValue: number) => {
    onChange(newValue);
  };

  const currentValue = value !== null ? value : (selector.default || selector.min_value || 0);

  return (
    <FormGroup
      label={selector.label || selector.name}
      labelInfo={selector.required ? '(required)' : ''}
      helperText={selector.description}
    >
      <Slider
        min={selector.min_value || 0}
        max={selector.max_value || 100}
        stepSize={selector.step || 1}
        labelStepSize={(selector.max_value || 100) - (selector.min_value || 0)}
        onChange={handleChange}
        value={currentValue}
        showTrackFill={true}
        labelRenderer={selector.show_value ? (val => String(val)) : false}
      />
    </FormGroup>
  );
};
