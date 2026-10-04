import Typography from '@mui/material/Typography';

import { PAGE_TITLES } from '../../constants/messageConstants';

export default function InsightsPage() {
  return (
    <Typography variant="h4" component="h1">
      {PAGE_TITLES.INSIGHTS}
    </Typography>
  );
}
