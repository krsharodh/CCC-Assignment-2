import { Helmet } from 'react-helmet';
import {
  Box,
  Container,
  Grid
} from '@material-ui/core';
import WordCloud from 'src/components/dashboard/Wordcloud';
import Map from 'src/components/dashboard/Map';
import Trend from 'src/components/dashboard/Trend';
const Dashboard = () => (
  <>
    <Helmet>
      <title>Dashboard | Material Kit</title>
    </Helmet>
    <Box
      sx={{
        backgroundColor: 'background.default',
        minHeight: '100%',
        py: 3
      }}
    >
      <Container maxWidth={false} spacing={3}>
          <Grid
            item
            lg={20}
            sm={10}
            xl={10}
            xs={8}
          >
            <WordCloud />
          </Grid>
        <Grid
            item
            lg={20}
            sm={10}
            xl={10}
            xs={8}
          >
          <Map />
        </Grid>
        <Grid
          item
          lg={20}
          sm={10}
          xl={10}
          xs={8}
        >
          <Trend />
        </Grid>
      </Container>
    </Box>
  </>
);

export default Dashboard;
