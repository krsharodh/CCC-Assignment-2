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

const CovidGraph2 = ({ city }) => {
    const data = [
        {
            "name": "1/01/2021",
            "tweets": 4000,
            "cases": 2400,
        },
        {
            "name": "2/01/2021",
            "tweets": 3000,
            "cases": 1398,
        },
        {
            "name": "3/01/2021",
            "tweets": 2000,
            "cases": 9800,
        },
        {
            "name": "4/01/2021",
            "tweets": 2780,
            "cases": 3908,
        },
        {
            "name": "5/01/2021",
            "tweets": 1890,
            "cases": 4800,
        },
        {
            "name": "6/01/2021",
            "tweets": 2390,
            "cases": 3800,
        },
        {
            "name": "7/01/2021",
            "tweets": 3490,
            "cases": 4300,
        }
    ]

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

function Wordcloud() {
    const words = [
        {
            text: 'word1',
            value: 64,
        },
        {
            text: 'word2',
            value: 11,
        },
        {
            text: 'word3',
            value: 16,
        },
        {
            text: 'bad',
            value: 17,
        },
        {
            text: 'Covid',
            value: 64,
        },
        {
            text: 'mistake',
            value: 11,
        },
        {
            text: 'thought',
            value: 16,
        },
        {
            text: 'bad',
            value: 17,
        }, {
            text: 'Covid',
            value: 64,
        },
        {
            text: 'mistake',
            value: 11,
        },
        {
            text: 'thought',
            value: 16,
        },
        {
            text: 'bad',
            value: 17,
        }, {
            text: 'Covid',
            value: 64,
        },
        {
            text: 'mistake',
            value: 11,
        },
        {
            text: 'thought',
            value: 16,
        },
        {
            text: 'bad',
            value: 17,
        }, {
            text: 'told',
            value: 64,
        },
        {
            text: 'mistake',
            value: 11,
        },
        {
            text: 'thought',
            value: 16,
        },
        {
            text: 'bad',
            value: 17,
        }, {
            text: 'Covid',
            value: 64,
        },
        {
            text: 'mistake',
            value: 11,
        },
        {
            text: 'thought',
            value: 16,
        },
        {
            text: 'bad',
            value: 17,
        },
    ]
    return <ReactWordcloud words={words} />
}


export { CovidGraph1, CovidGraph2, Wordcloud };