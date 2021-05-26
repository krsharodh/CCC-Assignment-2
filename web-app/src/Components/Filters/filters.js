import FormControl from '@material-ui/core/FormControl';
import MenuItem from '@material-ui/core/MenuItem';
import Select from '@material-ui/core/Select';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
    formControl: {
        margin: theme.spacing(1),
        minWidth: 120,
    },
    selectEmpty: {
        marginTop: theme.spacing(2),
    },
}));

function Filters({
    data,
    handleChange,
    value
}) {

    const classes = useStyles();

    return (
        <FormControl className={classes.formControl}>
            <Select
                // native
                // displayEmpty
                value={value}
                onChange={handleChange}
            >
                {/* <MenuItem value="">
                    <em>None</em>
                </MenuItem> */}
                {data.map(item => <MenuItem value={item.value}>{item.label}</MenuItem>)}
            </Select>
        </FormControl>
    );
}

export default Filters;
