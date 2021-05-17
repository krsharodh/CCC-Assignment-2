import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';

function Filters({
    autoCompleteList,
    label,
    handleChange,
    value
}) {

    return (
        <FormControl>
            <Select
                native
                displayEmpty
                value={value}
                onChange={handleChange}
                style={{ width: "100%" }}
            >
                {autoCompleteList.map(item => <option value={item.value}>{item.label}</option>)}
            </Select>
        </FormControl>
    );
}

export default Filters;
