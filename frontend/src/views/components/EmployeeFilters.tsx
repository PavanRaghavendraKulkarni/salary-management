import Button from '@mui/material/Button';
import MenuItem from '@mui/material/MenuItem';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';

import { ACTION_LABELS, FIELD_LABELS, FILTER_LABELS } from '../../constants/messageConstants';
import type {
  EmployeeFilterName,
  EmployeeFilterValues,
  FilterOptions,
} from '../../models/employee';

interface EmployeeFiltersProps {
  searchInput: string;
  filters: EmployeeFilterValues;
  filterOptions: FilterOptions;
  onSearchChange: (search: string) => void;
  onFilterChange: (name: EmployeeFilterName, value: string) => void;
  onClear: () => void;
}

const FILTER_FIELDS: { name: EmployeeFilterName; optionsKey: keyof FilterOptions }[] = [
  { name: 'country', optionsKey: 'countries' },
  { name: 'department', optionsKey: 'departments' },
  { name: 'job_title', optionsKey: 'job_titles' },
];

export default function EmployeeFilters({
  searchInput,
  filters,
  filterOptions,
  onSearchChange,
  onFilterChange,
  onClear,
}: EmployeeFiltersProps) {
  return (
    <Stack direction={{ xs: 'column', md: 'row' }} spacing={2} sx={{ mb: 2 }}>
      <TextField
        label={FILTER_LABELS.SEARCH}
        value={searchInput}
        onChange={(event) => onSearchChange(event.target.value)}
        size="small"
        type="search"
        sx={{ minWidth: 240, flexGrow: 1 }}
      />
      {FILTER_FIELDS.map(({ name, optionsKey }) => (
        <TextField
          key={name}
          select
          label={FIELD_LABELS[name]}
          value={filters[name]}
          onChange={(event) => onFilterChange(name, event.target.value)}
          size="small"
          sx={{ minWidth: 180 }}
        >
          <MenuItem value="">{FILTER_LABELS.ALL}</MenuItem>
          {filterOptions[optionsKey].map((option) => (
            <MenuItem key={option} value={option}>
              {option}
            </MenuItem>
          ))}
        </TextField>
      ))}
      <Button onClick={onClear} sx={{ whiteSpace: 'nowrap' }}>
        {ACTION_LABELS.CLEAR_FILTERS}
      </Button>
    </Stack>
  );
}
