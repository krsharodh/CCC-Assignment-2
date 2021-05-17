import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    ResponsiveContainer,
    Tooltip,
    Label,
    LabelList,
    Legend,
    CartesianGrid
} from "recharts";

const CovidGraph1 = () => {
    const data = [
        { name: "Melbourne", remaining: 1000, covid: 335 },
        { name: "Brisbane", remaining: 1000, covid: 345 },
        {
            name: "Perth",
            remaining: 1000,
            covid: 2110
        },
        {
            name: "Adelaide",
            remaining: 1000,
            covid: 540
        },
        {
            name: "Hobart",
            remaining: 1000,
            covid: 335
        },
        { name: "Darwin", remaining: 1000, covid: 110 },
        { name: "Canberra", remaining: 1000, covid: 110 }
    ];

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

const CovidGraph2 = () => {
    const data = [{ name: 'Page A', uv: 400, pv: 2400, amt: 2400 }];

    return (
        <BarChart width={730} height={250} data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="pv" fill="#8884d8" />
            <Bar dataKey="uv" fill="#82ca9d" />
        </BarChart>
    );
}


export { CovidGraph1, CovidGraph2 };