from coviz_helper import load_data, process_data, construct_doubling_text
import plotly.graph_objects as go


def _load_data():
    counties_df = load_data("us-counties.csv")
    data_by_county = {}
    for state in counties_df.state.unique():
        state_df = counties_df[counties_df.state == state]
        data_by_county[state] = {}
        for county in state_df.county.unique():
            county_df = state_df[state_df.county == county]
            if len(county_df) > 2 and county != "Unknown":
                data_by_county[state][county] = process_data(county_df)
        if not data_by_county[state]:
            data_by_county.pop(state)
    return data_by_county


def plot_data_by_county(
    initial_state = "California",
    initial_county = "Santa Clara",
):
    data_by_county = _load_data()
    county_list_by_state = [
        (state, sorted(state_data.keys()))
        for state, state_data in data_by_county.items()
    ]
    county_list_by_state.sort(key=lambda v : v[0])
    doubling_text = {}
    for state, counties in county_list_by_state:
        doubling_text[state] = {}
        for county in counties:
            case_counts = data_by_county[state][county][1]
            doubling_text[state][county] = construct_doubling_text(
                case_counts[-1], case_counts[0], len(case_counts)
            )

    fig = go.Figure()
    initial_data = data_by_county[initial_state][initial_county]
    fig.add_trace(go.Scatter(x=initial_data[0], y=initial_data[1], name ='actual', mode='markers'))
    fig.add_trace(go.Scatter(x=initial_data[0], y=initial_data[2], name = 'model', mode='lines'))

    state_idx = next(
        i for i,data_by_state in enumerate(county_list_by_state)
        if data_by_state[0] == initial_state
    )
    county_idx = next(
        i for i,county in enumerate(county_list_by_state[state_idx][1])
        if county == initial_county
    )

    buttons = {
        state: [
            dict(
                args=[
                    {
                        "x": [data_by_county[state][county][0], data_by_county[state][county][0]],
                        "y": [data_by_county[state][county][1], data_by_county[state][county][2]],
                    },
                    {
                        "xaxis.title": doubling_text[state][county],
                    },                
                ],
                label=county,
                method="update",
            )
            for county in counties
        ]
        for state, counties in county_list_by_state
    }

    fig.update_layout(
        title=dict(
            text="Covid cases by county over time",
            x=0.5,
            xanchor="center",
            yanchor="top",
            y=1,
            pad={"t": 20}
        ),
        updatemenus=[
            dict(
                buttons=[
                    dict(
                        args=[
                            {
                                "x": [data_by_county[state][counties[0]][0], data_by_county[state][counties[0]][0]],
                                "y": [data_by_county[state][counties[0]][1], data_by_county[state][counties[0]][2]],
                            },
                            {
                                "xaxis.title": doubling_text[state][counties[0]],
                                "updatemenus[1].buttons": buttons[state],
                                "updatemenus[1].active": 0,
                            },
                        ],
                        label=state,
                        method="update",
                    )
                    for state, counties in county_list_by_state
                ],
                active=state_idx,
                direction="down",
                pad={"r": 10, "t": -10},
                showactive=True,
                x=0.1,
                xanchor="left",
                y=1.1,
                yanchor="top"
            ),
            dict(
                buttons=buttons[initial_state],
                direction="down",
                pad={"r": 10, "t": -10},
                active=county_idx,
                showactive=True,
                x=0.7,
                xanchor="left",
                y=1.1,
                yanchor="top"
            ),
        ],
        annotations=[
            dict(
                x=0.03,
                y=1.1,
                xref="paper",
                yref="paper",
                text="State:",
                showarrow=False,
                yanchor="top",
                xanchor="left",
                font=dict(size=13),
            ),
            dict(
                x=0.62,
                y=1.1,
                xref="paper",
                yref="paper",
                text="County:",
                showarrow=False,
                yanchor="top",
                xanchor="left",
                font=dict(size=13),
            ),

        ],
        height = 600,
        margin=dict(t=100),
        xaxis_title=doubling_text[initial_state][initial_county],
        yaxis_title="# of cases",
    )

    fig.show()


