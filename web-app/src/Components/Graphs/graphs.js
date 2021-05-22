import {
    BarChart,
    Bar,
    LineChart,
    Line,
    XAxis,
    YAxis,
    ResponsiveContainer,
    Tooltip,
    Label,
    LabelList,
    Legend,
    CartesianGrid
} from "recharts";
import ReactWordcloud from 'react-wordcloud';

const CovidGraph1 = ({ data }) => {

    const renderCustomizedLabel = (props) => {
        const { content, ...rest } = props;
        return <Label {...rest} fontSize="12" fill="white" fontWeight="Bold" value={`${rest.value} %`} />;
    };

    return (
        <ResponsiveContainer height={250} width={"100%"}>
            <BarChart
                layout="vertical"
                data={data}
                margin={{ left: 10, right: 10 }}
            >
                <XAxis hide type="number" />
                <YAxis
                    type="category"
                    dataKey="city"
                    stroke="black"
                    fontSize="12"
                />
                <Tooltip />
                <Bar dataKey="percentage" fill="#ff6361" stackId="a">
                    <LabelList
                        dataKey="percentage"
                        position="center"
                        content={renderCustomizedLabel}
                    />
                </Bar>
                {/* <Bar dataKey="total_tweets" fill="#82ba7f" stackId="a">
                    <LabelList
                        dataKey="total_tweets"
                        position="center"
                        content={renderCustomizedLabel}
                    />
                </Bar> */}
            </BarChart>
        </ResponsiveContainer>
    );
}

const CovidGraph2 = ({ data }) => {

    return (
        <ResponsiveContainer height={250} width={"100%"}>

            <LineChart data={data} margin={{ left: 10, right: 10 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis hide dataKey="name" />
                <YAxis type="number" domain={[0, 'auto']} />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="cases" stroke="#8884d8" dot={false} />
                <Line type="monotone" dataKey="tweets" stroke="#82ca9d" dot={false} />
            </LineChart>
        </ResponsiveContainer>
    );
}

const Wordcloud = ({ data }) => {
    return <ReactWordcloud words={data} />
}

const JobGraph = ({ data }) => {

    const renderCustomizedLabel = (props) => {
        const { content, ...rest } = props;
        return <Label {...rest} fontSize="12" fill="white" fontWeight="Bold" />;
    };

    return (
        <ResponsiveContainer height={250} width={"100%"}>
            <BarChart
                layout="vertical"
                data={data}
                margin={{ left: 10, right: 10 }}
                stackOffset="expand"
            >
                <XAxis hide type="number" />
                <YAxis
                    type="category"
                    dataKey="city"
                    stroke="black"
                    fontSize="12"
                />
                <Tooltip />
                <Bar dataKey="metioned_jobkeeper" fill="#ff6361" stackId="a">
                    <LabelList
                        dataKey="metioned_jobkeeper"
                        position="center"
                        content={renderCustomizedLabel}
                    />
                </Bar>
                <Bar dataKey="median_weekly_personal_income" fill="#82ba7f" stackId="a">
                    <LabelList
                        dataKey="median_weekly_personal_income"
                        position="center"
                        content={renderCustomizedLabel}
                    />
                </Bar>
            </BarChart>
        </ResponsiveContainer>
    );
}


export { CovidGraph1, CovidGraph2, Wordcloud, JobGraph };