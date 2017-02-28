<?php

/*
 * This file is part of AppFlow.
 *
 * (c) Ivo Marino <ivo.marino@ttss.ch>
 *     Luca Di Maio <luca.dimaio@ttss.ch>
 *
 * For the full copyright and license information, please view the LICENSE
 * file that was distributed with this source code.
 *
 * NOTE: This is just an example layout.
 */

namespace AppFlow;

use AppFlow\Foo\Bar;

/**
 * @author Ivo Marino <ivo.marino@ttss.ch>
 * @author Luca Di Maio <luca.dimaio@ttss.ch>
 */
class AppFlow
{
    const VERSION = '@foo_version@';

    /**
     * @var Foo\Bar
     */
    private $foo;

    /**
     * @param  Foo\FooInterface $foo
     * @return void
     */
    public function setFoo(FooInterface $foo)
    {
        $this->foo = $foo;
    }
}
