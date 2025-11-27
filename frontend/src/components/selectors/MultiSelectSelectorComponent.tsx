/**
 * Multi-select selector component using Blueprint MultiSelect.
 */

import React from 'react';
import { FormGroup, Tag } from '@blueprintjs/core';
import { MultiSelect, type ItemRenderer } from '@blueprintjs/select';
import type { MultiSelectSchema } from '../../types/dashboard';

interface MultiSelectSelectorComponentProps {
  selector: MultiSelectSchema;
  value: (string | number)[] | null;
  onChange: (value: (string | number)[] | null) => void;
}

interface SelectOption {
  value: string | number;
  label: string;
}

const OptionMultiSelect = MultiSelect.ofType<SelectOption>();

export const MultiSelectSelectorComponent: React.FC<MultiSelectSelectorComponentProps> = ({
  selector,
  value,
  onChange,
}) => {
  // Parse options
  const options: SelectOption[] = (selector.options || []).map(opt => {
    if (typeof opt === 'object' && opt !== null && 'value' in opt) {
      return {
        value: opt.value,
        label: opt.label || String(opt.value)
      };
    }
    return {
      value: opt,
      label: String(opt)
    };
  });

  const currentValue = value !== null ? value : (selector.default || []);
  const selectedOptions = options.filter(opt => currentValue.includes(opt.value));

  const handleSelect = (item: SelectOption) => {
    const newValue = [...currentValue, item.value];
    onChange(newValue);
  };

  const handleRemove = (item: SelectOption) => {
    const newValue = currentValue.filter(v => v !== item.value);
    onChange(newValue.length > 0 ? newValue : null);
  };

  const renderOption: ItemRenderer<SelectOption> = (item, { handleClick, modifiers }) => {
    if (!modifiers.matchesPredicate) {
      return null;
    }
    return (
      <div
        key={String(item.value)}
        onClick={handleClick}
        style={{
          padding: '8px 12px',
          cursor: 'pointer',
          backgroundColor: modifiers.active ? '#f5f5f5' : 'white'
        }}
      >
        {item.label}
      </div>
    );
  };

  const renderTag = (item: SelectOption) => item.label;

  return (
    <FormGroup
      label={selector.label || selector.name}
      labelInfo={selector.required ? '(required)' : ''}
      helperText={selector.description}
    >
      <OptionMultiSelect
        items={options}
        selectedItems={selectedOptions}
        onItemSelect={handleSelect}
        itemRenderer={renderOption}
        tagRenderer={renderTag}
        tagInputProps={{
          onRemove: (value, index) => {
            const item = selectedOptions[index];
            if (item) {
              handleRemove(item);
            }
          },
        }}
        placeholder="Select items..."
        fill
      />
    </FormGroup>
  );
};
