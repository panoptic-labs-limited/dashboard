/**
 * Date selector component using Blueprint DateInput.
 */

import React from 'react';
import { FormGroup } from '@blueprintjs/core';
import { DateInput3 } from '@blueprintjs/datetime2';
import type { DateSelectorSchema } from '../../types/dashboard';

interface DateSelectorComponentProps {
  selector: DateSelectorSchema;
  value: string | null;
  onChange: (value: string | null) => void;
}

export const DateSelectorComponent: React.FC<DateSelectorComponentProps> = ({
  selector,
  value,
  onChange,
}) => {
  const handleChange = (selectedDate: string | null) => {
    if (selectedDate) {
      // Convert to ISO date string (YYYY-MM-DD)
      onChange(selectedDate);
    } else {
      onChange(null);
    }
  };

  const parseDate = (str: string): Date => new Date(str);
  const formatDate = (date: Date): string => date.toISOString().split('T')[0];

  return (
    <FormGroup
      label={selector.label || selector.name}
      labelInfo={selector.required ? '(required)' : ''}
      helperText={selector.description}
    >
      <DateInput3
        value={value || selector.default || ''}
        onChange={handleChange}
        parseDate={parseDate}
        formatDate={formatDate}
        placeholder="YYYY-MM-DD"
        fill={true}
        dateFnsFormat="yyyy-MM-dd"
      />
    </FormGroup>
  );
};
