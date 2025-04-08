type program = {
    weeks: [
        {
            week: number;
            days: [
                {
                    day: "monday" | "tuesday" | "wednesday" | "thursday" | "friday" | "saturday" | "sunday";
                    run_title: string;
                    run_description: string;
                }
            ]
        }
    ]
}

const testProgram = {
    weeks: [
        {
            week: 1,
            days: [
                {
                    day: "tuesday",
                    workouts: [
                        {
                            activity: "run",
                            type: "easy",
                            day: "tuesday",
                            distance: 6
                        }
                    ]
                },
                {
                    day: "wednesday",
                    workouts: [
                        {
                            activity: "run",
                            type: "intervals",
                            day: "tuesday",
                            distance: 8
                        }
                    ]
                }
            ]
        }
    ]
}
