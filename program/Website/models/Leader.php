<?php

class Leader{
    public $id;
    public $photos = [];

    function __construct($data)
    {
        $this->id = $data['id'];
        $this->photos = $data['photos'];
    }
}