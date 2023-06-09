<?php

class Country
{
    public $id;
    public $leader;
    public $position;
    public $photo;
    public $photo2;
    public $country_flag;

    function __construct($data)
    {
        $this->id = $data["id"];
        $this->leader = $data["leader"];
        $this->position = $data["position"];
        $this->photo = $data["photo"];
        $this->photo2 = $data["photo2"];
        $this->country_flag = $data["country_flag"];
    }
}
