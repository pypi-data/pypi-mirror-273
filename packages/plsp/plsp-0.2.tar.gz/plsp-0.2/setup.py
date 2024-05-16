from templated_setup import templated_setup

templated_setup.Setup_Helper.init(".templated_setup.cache.json")
templated_setup.Setup_Helper.setup(
	"plsp",
	"matrikater (Joel Watson)",
	"A simple, easy to use, and powerful logging library for Python.", **{
		"install_requires": ["templated_setup"],
	}
)
