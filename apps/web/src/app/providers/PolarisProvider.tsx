'use client';

import { AppProvider } from '@shopify/polaris';
import '@shopify/polaris/build/esm/styles.css';

export function PolarisProvider({ children }: { children: React.ReactNode }) {
  return (
    <AppProvider
      i18n={{
        Polaris: {
          Common: {
            checkbox: 'checkbox',
            undo: 'undo',
            cancel: 'cancel',
            clear: 'clear',
            submit: 'submit',
            more: 'more',
            search: 'search',
            delete: 'delete',
            edit: 'edit',
            close: 'close',
            remove: 'remove',
            add: 'add',
            save: 'save',
            select: 'select',
            confirm: 'confirm',
            replace: 'replace',
            view: 'view',
            manage: 'manage',
            copy: 'copy',
            duplicate: 'duplicate',
            refresh: 'refresh',
            move: 'move',
            filter: 'filter',
            sort: 'sort',
            searchPlaceholder: 'Search',
            noResultsFound: 'No results found',
            noResultsFor: 'No results for "{{searchTerm}}"',
            clearAll: 'Clear all',
            clearAllFilters: 'Clear all filters',
            clearSelection: 'Clear selection',
            clearFilters: 'Clear filters',
            clearSearch: 'Clear search',
            clearSort: 'Clear sort',
            clearView: 'Clear view',
            clearAllData: 'Clear all data',
            clearAllSelections: 'Clear all selections',
            clearAllFiltersAndSort: 'Clear all filters and sort',
            clearAllFiltersAndSearch: 'Clear all filters and search',
            clearAllFiltersAndView: 'Clear all filters and view',
            clearAllFiltersAndData: 'Clear all filters and data',
            clearAllSelectionsAndFilters: 'Clear all selections and filters',
            clearAllSelectionsAndSort: 'Clear all selections and sort',
            clearAllSelectionsAndView: 'Clear all selections and view',
            clearAllSelectionsAndData: 'Clear all selections and data',
            clearAllFiltersAndSortAndView: 'Clear all filters, sort, and view',
            clearAllFiltersAndSortAndData: 'Clear all filters, sort, and data',
            clearAllFiltersAndSearchAndView: 'Clear all filters, search, and view',
            clearAllFiltersAndSearchAndData: 'Clear all filters, search, and data',
            clearAllSelectionsAndFiltersAndSort: 'Clear all selections, filters, and sort',
            clearAllSelectionsAndFiltersAndView: 'Clear all selections, filters, and view',
            clearAllSelectionsAndFiltersAndData: 'Clear all selections, filters, and data',
            clearAllSelectionsAndSortAndView: 'Clear all selections, sort, and view',
            clearAllSelectionsAndSortAndData: 'Clear all selections, sort, and data',
            clearAllSelectionsAndViewAndData: 'Clear all selections, view, and data',
            clearAllFiltersAndSortAndViewAndData: 'Clear all filters, sort, view, and data',
            clearAllSelectionsAndFiltersAndSortAndView: 'Clear all selections, filters, sort, and view',
            clearAllSelectionsAndFiltersAndSortAndData: 'Clear all selections, filters, sort, and data',
            clearAllSelectionsAndFiltersAndViewAndData: 'Clear all selections, filters, view, and data',
            clearAllSelectionsAndSortAndViewAndData: 'Clear all selections, sort, view, and data',
            clearAllSelectionsAndFiltersAndSortAndViewAndData: 'Clear all selections, filters, sort, view, and data',
          },
        },
      }}
    >
      {children}
    </AppProvider>
  );
}
