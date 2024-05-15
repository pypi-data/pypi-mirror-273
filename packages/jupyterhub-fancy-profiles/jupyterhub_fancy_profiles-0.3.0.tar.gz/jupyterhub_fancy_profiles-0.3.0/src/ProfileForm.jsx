import { useContext, useState } from "react";
import "../node_modules/xterm/css/xterm.css";

import "./form.css";
import { SpawnerFormContext } from "./state";
import { ProfileOptions } from "./ProfileOptions";

/**
 * Generates the *contents* of the form shown in the profile selection page
 *
 * A <form> tag and a submit button are already included by JupyterHub, and should not
 * be generated here.
 */
function Form() {
  // Currently, we only support a single profile, with many options.
  const {
    profile: selectedProfile,
    setProfile,
    profileList,
  } = useContext(SpawnerFormContext);

  const [formError, setFormError] = useState("");

  const handleSubmit = (e) => {
    setFormError("");
    const form = e.target.closest("form");

    // validate the form
    const formIsValid = form.checkValidity();

    // prevent form submit
    if (!formIsValid) {
      setFormError(!selectedProfile ? "Select a container profile" : "");
      e.preventDefault();
    }
  };

  const handleProfileSelect = (e) => {
    const slug = e.target.value;
    setProfile(slug);
    setFormError("");
  };

  return (
    <fieldset
      aria-label="Select profile"
      aria-description="First, select the profile; second, configure the options for the selected profile."
    >
      {formError && <div className="profile-form-error">{formError}</div>}
      <input
        type="radio"
        className="hidden"
        name="profile"
        value={selectedProfile?.slug}
        checked
        readOnly
      />
      {profileList.map((profile) => {
        const { display_name, description, profile_options, slug } = profile;

        return (
          <div key={slug} className="profile-select">
            <div className="profile-select-radio">
              <input
                type="radio"
                name="select-profile"
                id={`profile-option-${slug}`}
                value={slug}
                onChange={handleProfileSelect}
                required
              />
              <label htmlFor={`profile-option-${slug}`}>
                {display_name} ({description})
              </label>
            </div>
            <ProfileOptions profile={slug} config={profile_options} />
          </div>
        );
      })}
      <button
        className="btn btn-jupyter form-control"
        type="submit"
        onClick={handleSubmit}
      >
        Start
      </button>
    </fieldset>
  );
}

export default Form;
