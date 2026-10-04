import Typography from '@mui/material/Typography';

import { PAGE_TITLES } from '../../constants/messageConstants';

export default function EmployeesPage() {
  return (
    <Typography variant="h4" component="h1">
      {PAGE_TITLES.EMPLOYEES}
    </Typography>
  );
}
