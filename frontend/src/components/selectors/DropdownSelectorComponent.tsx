/**
 * Dropdown selector component using Blueprint Select.
 */

import React from 'react';
import { FormGroup, HTMLSelect } from '@blueprintjs/core';
import type { DropdownSelectorSchema } from '../../types/dashboard';

interface DropdownSelectorComponentProps {
  selector: DropdownSelectorSchema;
  value: string | number | null;
  onChange: (value: string | number | null) => void;
}

export const DropdownSelectorComponent: React.FC<DropdownSelectorComponentProps> = ({
  selector,
  value,
  onChange,
}) => {
  const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const newValue = event.target.value;
    onChange(newValue || null);
  };

  const currentValue = value !== null ? value : (selector.default || '');

  return (
    <FormGroup
      label={selector.label || selector.name}
      labelInfo={selector.required ? '(required)' : ''}
      helperText={selector.description}
    >
      <HTMLSelect
        value={currentValue}
        onChange={handleChange}
        fill={true}
        options={[
          { label: 'Select...', value: '' },
          ...(selector.options || []).map(opt => ({
            label: String(opt),
            value: opt
          }))
        ]}
      />
    </FormGroup>
  );
};
