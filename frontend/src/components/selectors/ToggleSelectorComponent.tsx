/**
 * Toggle (switch/checkbox) selector component using Blueprint Switch.
 */

import React from 'react';
import { FormGroup, Switch } from '@blueprintjs/core';
import type { ToggleSchema } from '../../types/dashboard';

interface ToggleSelectorComponentProps {
  selector: ToggleSchema;
  value: boolean | null;
  onChange: (value: boolean | null) => void;
}

export const ToggleSelectorComponent: React.FC<ToggleSelectorComponentProps> = ({
  selector,
  value,
  onChange,
}) => {
  const handleChange = (event: React.FormEvent<HTMLInputElement>) => {
    onChange(event.currentTarget.checked);
  };

  const currentValue = value !== null ? value : (selector.default || false);

  return (
    <FormGroup
      label={selector.label || selector.name}
      helperText={selector.description}
    >
      <Switch
        checked={currentValue}
        onChange={handleChange}
        large
      />
    </FormGroup>
  );
};
