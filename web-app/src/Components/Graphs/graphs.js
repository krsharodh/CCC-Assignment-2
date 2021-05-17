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

        return <Label {...rest} fontSize="12" fill="#FFFFFF" fontWeight="Bold" />;
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
                    dataKey="name"
                    stroke="black"
                    fontSize="12"
                />
                <Tooltip />
                <Bar dataKey="remaining" fill="#dd7876" stackId="a">
                    <LabelList
                        dataKey="remaining"
                        position="center"
                        content={renderCustomizedLabel}
                    />
                </Bar>
                <Bar dataKey="covid" fill="#82ba7f" stackId="a">
                    <LabelList
                        dataKey="covid"
                        position="center"
                        content={renderCustomizedLabel}
                    />
                </Bar>
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
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="cases" stroke="#8884d8" />
                <Line type="monotone" dataKey="tweets" stroke="#82ca9d" />
            </LineChart>
        </ResponsiveContainer>
    );
}

const Wordcloud = ({ data }) => {
    return <ReactWordcloud words={data} />
}


export { CovidGraph1, CovidGraph2, Wordcloud };