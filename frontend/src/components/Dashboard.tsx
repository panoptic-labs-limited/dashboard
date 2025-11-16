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
import type {
  PageSchema,
  SectionSchema,
  RowSchema,
  ColumnSchema,
  SelectorLayoutSchema,
  WidgetSchema,
  SelectorSchema,
} from '../types/dashboard';

interface DashboardProps {
  dashboardName: string;
}

export const Dashboard: React.FC<DashboardProps> = ({ dashboardName }) => {
  const { data: dashboard, isLoading, error } = useDashboard(dashboardName);
  const [selectorValues, setSelectorValues] = useState<Record<string, any>>({});
  const [selectedPageId, setSelectedPageId] = useState<string>('');
  const [collapsedSections, setCollapsedSections] = useState<Set<string>>(new Set());

  // Extract all selectors from dashboard structure
  const selectors = useMemo(() => {
    if (!dashboard) return [];
    const selectorList: Array<{ id: string; selector: SelectorSchema }> = [];

    const extractSelectors = (node: any) => {
      if (!node) return;

      if (node.type === 'selector' && node.selector) {
        selectorList.push({ id: node.id, selector: node.selector });
      }

      // Recursively search children
      if (node.children && Array.isArray(node.children)) {
        node.children.forEach(extractSelectors);
      }
      if (node.sections && Array.isArray(node.sections)) {
        node.sections.forEach(extractSelectors);
      }
      if (node.pages && Array.isArray(node.pages)) {
        node.pages.forEach(extractSelectors);
      }
    };

    extractSelectors(dashboard.structure);
    return selectorList;
  }, [dashboard]);

  // Initialize selector values with defaults
  useEffect(() => {
    if (selectors.length > 0 && Object.keys(selectorValues).length === 0) {
      const defaults: Record<string, any> = {};
      selectors.forEach(({ selector }) => {
        if (selector.default !== undefined && selector.default !== null) {
          defaults[selector.name] = selector.default;
        }
      });
      setSelectorValues(defaults);
    }
  }, [selectors]);

  // Set initial page selection
  useEffect(() => {
    if (dashboard && !selectedPageId && dashboard.structure.pages.length > 0) {
      setSelectedPageId(dashboard.structure.pages[0].id);
    }
  }, [dashboard, selectedPageId]);

  // Handle selector value change
  const handleSelectorChange = (name: string, value: any) => {
    setSelectorValues(prev => ({ ...prev, [name]: value }));
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

  // Render selector
  const renderSelector = (selectorLayout: SelectorLayoutSchema) => {
    const { selector } = selectorLayout;
    const value = selectorValues[selector.name];

    switch (selector.selector_type) {
      case 'date':
        return (
          <DateSelectorComponent
            key={selectorLayout.id}
            selector={selector}
            value={value || null}
            onChange={(val) => handleSelectorChange(selector.name, val)}
          />
        );

      case 'dropdown':
        return (
          <DropdownSelectorComponent
            key={selectorLayout.id}
            selector={selector}
            value={value || null}
            onChange={(val) => handleSelectorChange(selector.name, val)}
          />
        );

      default:
        return (
          <div key={selectorLayout.id}>
            Unsupported selector type: {selector.selector_type}
          </div>
        );
    }
  };

  // Render widget
  const renderWidget = (widget: WidgetSchema) => {
    return (
      <div key={widget.id} style={{ gridColumn: '1 / -1' }}>
        <WidgetContainer
          dashboardName={dashboardName}
          widget={widget}
          selectorValues={selectorValues}
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
          gridColumn: column.width ? `span ${getColumnSpan(column.width)}` : '1 / -1',
        }}
      >
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {column.children.map(child => {
            if (child.type === 'widget') {
              return renderWidget(child as WidgetSchema);
            } else if (child.type === 'selector') {
              // Skip rendering selectors in the layout - they're already in the selector panel
              return null;
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
          display: 'grid',
          gridTemplateColumns: 'repeat(12, 1fr)',
          gap: '20px',
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
        {page.sections.map(renderSection)}
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

  const selectedPage = dashboard.structure.pages.find(p => p.id === selectedPageId);

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

      {/* Selector panel */}
      {selectors.length > 0 && (
        <Card elevation={Elevation.TWO} style={{ marginBottom: '20px', padding: '20px' }}>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
            gap: '20px',
          }}>
            {selectors.map(({ id, selector }) => (
              <div key={id}>{renderSelector({ id, type: 'selector', selector })}</div>
            ))}
          </div>
        </Card>
      )}

      {/* Pages (tabs) */}
      {dashboard.structure.pages.length > 1 ? (
        <Tabs
          id="dashboard-pages"
          selectedTabId={selectedPageId}
          onChange={(newTabId) => setSelectedPageId(newTabId as string)}
          renderActiveTabPanelOnly={false}
        >
          {dashboard.structure.pages.map(page => (
            <Tab key={page.id} id={page.id} title={page.title} panel={renderPage(page)} />
          ))}
        </Tabs>
      ) : (
        selectedPage && renderPage(selectedPage)
      )}
    </div>
  );
};
