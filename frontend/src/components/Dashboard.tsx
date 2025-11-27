/**
 * Main Dashboard component.
 */

import React, { useState, useEffect, useMemo } from 'react';
import {
  Card,
  Elevation,
  Spinner,
  Intent,
  Callout,
  Tabs,
  Tab,
  Collapse,
  Icon,
} from '@blueprintjs/core';
import { useDashboard } from '../hooks/useDashboard';
import { WidgetContainer } from './WidgetContainer';
import { DateSelectorComponent } from './selectors/DateSelectorComponent';
import { DropdownSelectorComponent } from './selectors/DropdownSelectorComponent';
import { ToggleSelectorComponent } from './selectors/ToggleSelectorComponent';
import { MultiSelectSelectorComponent } from './selectors/MultiSelectSelectorComponent';
import { SliderSelectorComponent } from './selectors/SliderSelectorComponent';
import type {
  PageSchema,
  SectionSchema,
  RowSchema,
  ColumnSchema,
  WidgetSchema,
  InputSchema,
} from '../types/dashboard';

interface DashboardProps {
  dashboardName: string;
}

export const Dashboard: React.FC<DashboardProps> = ({ dashboardName }) => {
  const { data: dashboard, isLoading, error } = useDashboard(dashboardName);
  const [inputValues, setInputValues] = useState<Record<string, any>>({});
  const [selectedPageId, setSelectedPageId] = useState<string>('');
  const [collapsedSections, setCollapsedSections] = useState<Set<string>>(new Set());
  const [showFilters, setShowFilters] = useState<boolean>(false);

  // Extract all inputs from dashboard structure
  const inputs = useMemo(() => {
    if (!dashboard) return [];
    const inputList: Array<InputSchema> = [];

    const extractInputs = (node: any) => {
      if (!node) return;

      if (node.type === 'input') {
        inputList.push(node as InputSchema);
      }

      // Recursively search children
      if (node.children && Array.isArray(node.children)) {
        node.children.forEach(extractInputs);
      }
    };

    extractInputs(dashboard.structure);
    return inputList;
  }, [dashboard]);

  // Initialize input values with defaults
  useEffect(() => {
    if (inputs.length > 0 && Object.keys(inputValues).length === 0) {
      const defaults: Record<string, any> = {};
      inputs.forEach((input) => {
        if (input.default !== undefined && input.default !== null) {
          defaults[input.id] = input.default;
        }
      });
      setInputValues(defaults);
    }
  }, [inputs]);

  // Set initial page selection
  useEffect(() => {
    if (dashboard && !selectedPageId && dashboard.structure.children && dashboard.structure.children.length > 0) {
      setSelectedPageId(dashboard.structure.children[0].id);
    }
  }, [dashboard, selectedPageId]);

  // Handle input value change
  const handleInputChange = (id: string, value: any) => {
    setInputValues(prev => ({ ...prev, [id]: value }));
  };

  // Toggle section collapse
  const toggleSection = (sectionId: string) => {
    setCollapsedSections(prev => {
      const newSet = new Set(prev);
      if (newSet.has(sectionId)) {
        newSet.delete(sectionId);
      } else {
        newSet.add(sectionId);
      }
      return newSet;
    });
  };

  // Render input
  const renderInput = (input: InputSchema) => {
    const value = inputValues[input.id];

    switch (input.input_type) {
      case 'date':
        return (
          <DateSelectorComponent
            key={input.id}
            selector={input as any} // TODO: Update component to use InputSchema
            value={value || null}
            onChange={(val) => handleInputChange(input.id, val)}
          />
        );

      case 'select':
        return (
          <DropdownSelectorComponent
            key={input.id}
            selector={input as any} // TODO: Update component to use InputSchema
            value={value || null}
            onChange={(val) => handleInputChange(input.id, val)}
          />
        );

      case 'toggle':
        return (
          <ToggleSelectorComponent
            key={input.id}
            selector={input as any}
            value={value || null}
            onChange={(val) => handleInputChange(input.id, val)}
          />
        );

      case 'multi_select':
        return (
          <MultiSelectSelectorComponent
            key={input.id}
            selector={input as any}
            value={value || null}
            onChange={(val) => handleInputChange(input.id, val)}
          />
        );

      case 'slider':
        return (
          <SliderSelectorComponent
            key={input.id}
            selector={input as any}
            value={value || null}
            onChange={(val) => handleInputChange(input.id, val)}
          />
        );

      default:
        return (
          <div key={input.id}>
            Unsupported input type: {input.input_type}
          </div>
        );
    }
  };

  // Render widget
  const renderWidget = (widget: WidgetSchema) => {
    return (
      <div key={widget.id}>
        <WidgetContainer
          dashboardName={dashboardName}
          widget={widget}
          inputValues={inputValues}
        />
      </div>
    );
  };

  // Render column
  const renderColumn = (column: ColumnSchema) => {
    return (
      <div
        key={column.id}
        style={{
          flex: column.weight || 1,
        }}
      >
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {column.children.map(child => {
            if (child.type === 'widget') {
              return renderWidget(child as WidgetSchema);
            } else if (child.type === 'input') {
              // Render inputs inline
              return renderInput(child as InputSchema);
            } else if (child.type === 'row') {
              return renderRow(child as RowSchema);
            }
            return null;
          })}
        </div>
      </div>
    );
  };

  // Render row
  const renderRow = (row: RowSchema) => {
    return (
      <div
        key={row.id}
        style={{
          display: 'flex',
          gap: row.gap || '20px',
          alignItems: row.align || 'stretch',
        }}
      >
        {row.children.map(renderColumn)}
      </div>
    );
  };

  // Render section
  const renderSection = (section: SectionSchema) => {
    const isCollapsed = collapsedSections.has(section.id);

    // Check if section has any visible content (non-selector children)
    const hasVisibleContent = (node: any): boolean => {
      if (!node) return false;

      if (node.type === 'widget') return true;

      if (node.type === 'selector') return false;

      if (node.children && Array.isArray(node.children)) {
        return node.children.some(hasVisibleContent);
      }

      return false;
    };

    if (!section.children.some(hasVisibleContent)) {
      return null; // Skip empty sections
    }

    return (
      <Card key={section.id} elevation={Elevation.ONE} style={{ marginBottom: '20px' }}>
        {section.title && (
          <div
            onClick={() => section.collapsible && toggleSection(section.id)}
            style={{
              padding: '15px 20px',
              borderBottom: isCollapsed ? 'none' : '1px solid #e1e8ed',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              cursor: section.collapsible ? 'pointer' : 'default',
            }}
          >
            <h2 style={{ margin: 0, fontSize: '18px', fontWeight: 600 }}>
              {section.title}
            </h2>
            {section.collapsible && (
              <Icon icon={isCollapsed ? 'chevron-down' : 'chevron-up'} />
            )}
          </div>
        )}
        <Collapse isOpen={!isCollapsed}>
          <div style={{ padding: '20px' }}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
              {section.children.map(child => {
                if (child.type === 'row') {
                  return renderRow(child as RowSchema);
                } else if (child.type === 'column') {
                  return renderColumn(child as ColumnSchema);
                }
                return null;
              })}
            </div>
          </div>
        </Collapse>
      </Card>
    );
  };

  // Render page
  const renderPage = (page: PageSchema) => {
    return (
      <div>
        {page.description && (
          <Callout style={{ marginBottom: '20px' }}>{page.description}</Callout>
        )}
        {page.children && page.children.map(child => {
          if (child.type === 'section') {
            return renderSection(child as SectionSchema);
          } else if (child.type === 'row') {
            return renderRow(child as RowSchema);
          } else if (child.type === 'column') {
            return renderColumn(child as ColumnSchema);
          }
          return null;
        })}
      </div>
    );
  };

  // Helper to convert width spec to grid columns
  const getColumnSpan = (width: string): number => {
    const widthMap: Record<string, number> = {
      '1/1': 12,
      '1/2': 6,
      '1/3': 4,
      '2/3': 8,
      '1/4': 3,
      '3/4': 9,
      '1/6': 2,
      '5/6': 10,
    };
    return widthMap[width] || 12;
  };

  // Loading state
  if (isLoading) {
    return (
      <div style={{ padding: '40px', textAlign: 'center' }}>
        <Spinner size={50} />
        <div style={{ marginTop: '20px', fontSize: '16px', color: '#888' }}>
          Loading dashboard...
        </div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div style={{ padding: '40px' }}>
        <Callout intent={Intent.DANGER} title="Failed to load dashboard">
          {error.message}
        </Callout>
      </div>
    );
  }

  if (!dashboard) {
    return null;
  }

  const pages = dashboard.structure.children || [];
  const selectedPage = pages.find(p => p.id === selectedPageId);

  return (
    <div style={{ padding: '20px', maxWidth: '1400px', margin: '0 auto' }}>
      {/* Dashboard header */}
      <div style={{ marginBottom: '30px' }}>
        <h1 style={{ margin: 0, marginBottom: '10px', fontSize: '28px' }}>
          {dashboard.title}
        </h1>
        {dashboard.description && (
          <p style={{ margin: 0, color: '#5c7080', fontSize: '14px' }}>
            {dashboard.description}
          </p>
        )}
      </div>

      {/* Global filters panel */}
      {inputs.length > 0 && (
        <Card elevation={Elevation.TWO} style={{ marginBottom: '20px' }}>
          <div
            onClick={() => setShowFilters(!showFilters)}
            style={{
              padding: '12px 20px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '10px',
              borderBottom: showFilters ? '1px solid #e1e8ed' : 'none',
            }}
          >
            <Icon icon={showFilters ? 'chevron-down' : 'chevron-right'} />
            <span style={{ fontWeight: 500, fontSize: '14px' }}>
              Global Filters {!showFilters && `(${inputs.length})`}
            </span>
          </div>
          <Collapse isOpen={showFilters}>
            <div style={{ padding: '20px' }}>
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
                gap: '20px',
              }}>
                {inputs.map((input) => (
                  <div key={input.id}>{renderInput(input)}</div>
                ))}
              </div>
            </div>
          </Collapse>
        </Card>
      )}

      {/* Pages (tabs) */}
      {pages.length > 1 ? (
        <Tabs
          id="dashboard-pages"
          selectedTabId={selectedPageId}
          onChange={(newTabId) => setSelectedPageId(newTabId as string)}
          renderActiveTabPanelOnly={false}
        >
          {pages.map(page => (
            <Tab key={page.id} id={page.id} title={page.title} panel={renderPage(page)} />
          ))}
        </Tabs>
      ) : (
        selectedPage && renderPage(selectedPage)
      )}
    </div>
  );
};
